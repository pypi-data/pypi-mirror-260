
import pandas as pd

def find_best_hyperparams(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: str,
    n_trials: int = 10
) -> dict:
    """
    Find the best hyperparameters for the given `model_name`
    using Optuna's hyperparameter optimization
    """
    raise NotImplementedError

def sample_hyperparams(trial) -> dict:
    return {
        "n_estimators": trial.suggest_int("n_estimators", 10, 1000),
        "max_depth": trial.suggest_int("max_depth", 1, 32),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),
        "max_features": trial.suggest_categorical("max_features", ["auto", "sqrt", "log2"]),
    }