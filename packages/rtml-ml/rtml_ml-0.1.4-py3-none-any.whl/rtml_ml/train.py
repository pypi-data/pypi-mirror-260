from datetime import datetime, timedelta
import logging
from typing import Optional, Tuple, List
import os
import argparse

from comet_ml import Experiment
import pickle
import pandas as pd
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    classification_report,
)

from rtml_tools.logging import initialize_logger
from rtml_tools.config import YamlConfig
from rtml_ml.data import get_ohlc_data_from_store

# from rtml_ml.preprocessing import fill_missing_timestamps
from rtml_ml.preprocessing import (
    MissingValuesFiller,
    TargetColumnAdder
)
from rtml_ml.features import get_feature_engineering_pipeline
from rtml_ml.model_factory import get_model

logger = logging.getLogger()


def split_train_test(
    ts_data: pd.DataFrame,
    train_test_cutoff_date: datetime,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the given `ts_data` by its `timestamp`
    using the provided `train_test_cutoff_date`.
    """
    train_test_cutoff_ms = int(train_test_cutoff_date.timestamp() * 1000)

    ts_train = ts_data[ts_data['timestamp'] < train_test_cutoff_ms]
    ts_test = ts_data[ts_data['timestamp'] >= train_test_cutoff_ms]
    return ts_train, ts_test

def log_eval_metrics(
    y_test,
    y_pred,
    experiment: Experiment,    
):
    """
    Evaluate the model on the test data using
    - confusion matrix
    - accuracy
    - classification report
    """
    # confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    logger.info("Confusion Matrix:")
    logger.info(conf_matrix)
    experiment.log_confusion_matrix(
        matrix=conf_matrix,
        labels=['-1', '0', '1']
    )

    # accuracy
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Accuracy: {accuracy:.2%}")
    experiment.log_metric('accuracy', accuracy)

    # classification report
    class_report = classification_report(y_test, y_pred)
    logger.info("Classification Report:")
    logger.info(class_report)
    experiment.log_text(class_report)

def log_model_artifact(
    model: Pipeline,
    experiment: Experiment,
    product_id: str
):
    """
    Log the inference pipeline to the comet.ml server
    """
    # Save the model to a local file
    model_path = 'inference_pipeline.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # push the model to the comet.ml server
    model_name = f'{product_id.replace("/", "_")}_direction_predictor'
    logger.info(f"Logging the model to comet.ml as {model_name}")
    experiment.log_model(model_name, model_path)
    
    # register the model to the comet ML model registry
    experiment.register_model(model_name)
    # os.remove(model_path)

def train(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    train_test_cutoff_date: Optional[datetime] = None,
    product_id: Optional[str] = 'XBT/EUR',
    n_train_samples: Optional[int] = None,
    ohlc_window_seconds: Optional[int] = None,
    prediction_horizon_steps: Optional[int] = None,
    feature_view_params: Optional[dict] = None,
    history_horizon_steps: Optional[int] = None,

    model_name: Optional[str] = 'RandomForestClassifier',
    tune_hyperparams: Optional[bool] = False,
    hyperparam_search_trials: Optional[int] = 10,
):
    """
    - Gets OHLC data from the Feature store
    - Adds a target column
    - Trains a model
    - Saves the model in the model registry
    """
    experiment = Experiment(
        api_key=os.environ["COMET_API_KEY"],
        project_name=os.environ["COMET_PROJECT_NAME"],
        workspace=os.environ["COMET_WORKSPACE"],
    )

    if to_date is None:
        # to_date as current utc datetime rounded to the closest previous day
        to_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    if from_date is None:
        # from_date as current utc datetime minus 90 days
        from_date = to_date - timedelta(days=90)

    if train_test_cutoff_date is None:
        # train_test_cutoff_date as current utc datetime minus 30 days
        train_test_cutoff_date = to_date - timedelta(days=30)

    experiment.log_parameters({
        "from_date": from_date,
        "to_date": to_date,
        "train_test_cutoff_date": train_test_cutoff_date,
        "product_id": product_id,
        "ohlc_window_seconds": ohlc_window_seconds,
        "prediction_horizon_steps": prediction_horizon_steps,
        "history_horizon_steps": history_horizon_steps,
        # "feature_view_params": feature_view_params,
    })

    # TODO: maybe add wrapper around CometML API to log
    # dictionaries as usual parameters
    # save feature_view_params to local json file
    with open('feature_view_params.json', 'w') as f:
        import json
        json.dump(feature_view_params, f)
    experiment.log_asset('feature_view_params.json', file_name='feature_view_params')

    # fetch time-series OHLC data from the Feature Store
    ts_data = get_ohlc_data_from_store(
        from_date,
        to_date,
        product_id,
        feature_view_params,
        # global_config,
        cache_dir='../.cache/ohlc_data/',
    )
    experiment.log_dataset_hash(ts_data)
    
    # add datetime column from the timestamp columns
    ts_data['datetime'] = pd.to_datetime(ts_data['timestamp'], unit='ms')
    
    # split the data into training and test sets
    logger.info('Splitting the data into training and test sets')
    ts_train, ts_test = split_train_test(ts_data, train_test_cutoff_date)
    
    if n_train_samples:
        logger.info(f'Using only {n_train_samples} samples to train the model')
        ts_train = ts_train.head(n_train_samples)

    logger.info('Training set:')
    logger.info(f'  {len(ts_train):,} training samples')
    logger.info(f'  from {ts_train["datetime"].min()} to {ts_train["datetime"].max()}')
    
    logger.info('Test set:')
    logger.info(f'  {len(ts_test):,} test samples')
    logger.info(f'  from {ts_test["datetime"].min()} to {ts_test["datetime"].max()}')

    # preprocessing pipeline
    preprocessing_pipeline = Pipeline([
        ('missing_value_imputer', MissingValuesFiller(step_ms=ohlc_window_seconds*1000)),
        ('target_column_adder', TargetColumnAdder(window_size=prediction_horizon_steps)),
    ])
    ts_train = preprocessing_pipeline.fit_transform(ts_train)
    ts_test = preprocessing_pipeline.transform(ts_test)
    logger.info(f'{len(ts_train):,} training samples after filling missing timestamps')
    logger.info(f'{len(ts_test):,} test samples after filling missing timestamps')

    # check the target distribution in the training and test sets is balanced
    logger.info('Training set target distribution:')
    logger.info(f'{ts_train["target"].value_counts()}')
    logger.info('Test set target distribution:')
    logger.info(f'{ts_test["target"].value_counts()}')

    # feature engineering pipeline
    fe_pipeline = get_feature_engineering_pipeline()
    ts_train = fe_pipeline.fit_transform(ts_train)
    ts_test = fe_pipeline.transform(ts_test)

    # drop rows with NaN values
    ts_train = ts_train.dropna()
    ts_test = ts_test.dropna()
    logger.info(f'{len(ts_train):,} training samples after dropping NaN values')
    logger.info(f'{len(ts_test):,} test samples after dropping NaN values')

    # split the data into features and target
    X_train = ts_train.drop(columns=['target', 'timestamp'])
    y_train = ts_train['target']
    X_test = ts_test.drop(columns=['target', 'timestamp'])
    y_test = ts_test['target']
    logger.info(f'X_train.shape: {X_train.shape}')
    logger.info(f'y_train.shape: {y_train.shape}')
    logger.info(f'X_test.shape: {X_test.shape}')
    logger.info(f'y_test.shape: {y_test.shape}')

    experiment.log_parameter('features', X_train.columns.tolist())

    if tune_hyperparams:
        logger.info('Tuning hyperparameters')
        from rtml_ml.hyperparams import find_best_hyperparams
        best_hyperparams = find_best_hyperparams(
            X_train, y_train, model_name, hyperparam_search_trials)
        logger.info(f'Best hyperparameters: {best_hyperparams}')

        model = get_model(model_name, best_hyperparams)

    else:
        logger.info('Using default hyperparameters')
        model = get_model(model_name)

    # model training
    # model = RandomForestClassifier()
    model.fit(X_train, y_train)
    logger.info('Model training is DONE!')

    # model evaluation on test data
    y_pred = model.predict(X_test)
    log_eval_metrics(y_test, y_pred, experiment)

    # save preprocessing and model artifacts
    inference_pipeline = make_pipeline(
        preprocessing_pipeline.named_steps['missing_value_imputer'],
        fe_pipeline,
        model
    )
    log_model_artifact(inference_pipeline, experiment, product_id)
    logger.info('Model artifact logged to Experiment Tracker!')

    experiment.end()


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--from_date', type=str, required=False, default=None)
    parser.add_argument('--to_date', type=str, required=False, default=None)
    parser.add_argument('--train_test_cutoff_date', type=str, required=False, default=None)
    parser.add_argument('--product_id', type=str, required=False, default='XBT/EUR')
    parser.add_argument('--n_train_samples', type=int, required=False, default=None)
    parser.add_argument('--global-config-file', type=str, required=False, default='../config.yml')

    args = parser.parse_args()
    
    if args.from_date:
        args.from_date = datetime.strptime(args.from_date, '%Y-%m-%d')
    
    if args.to_date:
        args.to_date = datetime.strptime(args.to_date, '%Y-%m-%d')

    if args.train_test_cutoff_date:
        args.train_test_cutoff_date = datetime.strptime(args.train_test_cutoff_date, '%Y-%m-%d')

    return args


if __name__ == '__main__':

    initialize_logger()

    # Parse command line arguments
    args = parse_arguments()
    
    # Load parameters from global config file
    logger.info(f'Loading global parameters from {args.global_config_file}')
    yaml_config = YamlConfig(args.global_config_file)
    config = yaml_config._config['ml']

    # Train the model
    train(
        from_date=args.from_date,
        to_date=args.to_date,
        train_test_cutoff_date=args.train_test_cutoff_date,
        product_id=args.product_id,
        n_train_samples=args.n_train_samples,
        ohlc_window_seconds=yaml_config._config['ohlc_window_seconds'],
        prediction_horizon_steps=yaml_config._config['ml']['prediction_horizon_steps'],
        history_horizon_steps=yaml_config._config['ml']['history_horizon_steps'],
        feature_view_params=yaml_config.get_feature_view_params('ohlc_feature_view'),

        model_name=yaml_config._config['ml']['model_name'],
        tune_hyperparams=yaml_config._config['ml']['tune_hyperparams'],
        hyperparam_search_trials=yaml_config._config['ml']['hyperparam_search_trials'],
    )