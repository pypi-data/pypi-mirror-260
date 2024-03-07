from typing import Optional, List, Dict, Any
import pickle
import logging
from datetime import datetime, timezone
import pytz
import os

from typing_extensions import Self

import pandas as pd

from comet_ml import API
from sklearn.pipeline import Pipeline

from rtml_tools.feature_store_api.api import FeatureStore
from rtml_tools.feature_store_api.types import FeatureViewConfig

logger = logging.getLogger(__name__)

class Predictor:
    
    def __init__(
        self,
        model: Pipeline,        
        ohlc_window_seconds: int,
        product_id: str,
        history_horizon_steps: int,
        prediction_horizon_steps: int,
        feature_view_config: FeatureViewConfig,
    ):
        self.model = model
        self.ohlc_window_seconds = ohlc_window_seconds
        self.product_id = product_id
        self.history_horizon_steps = history_horizon_steps
        self.prediction_horizon_steps = prediction_horizon_steps
        self.feature_view_config = feature_view_config

        # get pointer to the feature view we need to read data from 
        self.feature_store = FeatureStore(
            api_key=os.environ["HOPSWORKS_API_KEY"],
            project_name=os.environ["HOPSWORKS_PROJECT_NAME"],
        )
        self.feature_view = self.feature_store.get_or_create_feature_view(feature_view_config)

    # @classmethod
    # def from_local_pickle(
    #     cls,
    #     model_path: str,
    #     # parameters_path: Optional[str] = None,
    # ):
    #     # TODO: example parameters
    #     ohlc_window_seconds = 60
    #     product_id = 'XBT/EUR'
    #     history_horizon_steps = 60
    #     prediction_horizon_steps = 5
        
    #     from rtml_tools.config import YamlConfig
    #     yaml_file = '/Users/paulabartabajo/src/real-time-ml-tutorial/config.yml'
    #     yaml_config = YamlConfig(yaml_file)
    #     fv_params = yaml_config.get_feature_view_params('ohlc_feature_view')
    #     fv_config = FeatureViewConfig.from_params(fv_params)
        
    #     return cls(
    #         local_pickle_path=model_path,
            
    #         ohlc_window_seconds=ohlc_window_seconds,
    #         product_id=product_id,
    #         history_horizon_steps=history_horizon_steps,
    #         prediction_horizon_steps=prediction_horizon_steps,

    #         feature_view_config=fv_config,
    #         # establish_feature_store_connection=True,
    #     )
    
    @classmethod
    def from_model_registry(cls, model_name):
        raise NotImplementedError
        # return cls()

    @classmethod
    def from_experiment_key(
        cls,
        experiment_key: str
    ) -> Self:
        """
        Loads the model and necessary metadata from the Comet ML experiment with
        the given `experiment_key`.
        """        

        # TODO: add wrapper around CometML to simplify this - START
        # load experiment from Comet ML
        api = API(api_key=os.environ["COMET_API_KEY"])
        experiment = api.get_experiment_by_key(experiment_key)
        
        # read parameters
        ohlc_window_seconds = int(experiment.get_parameters_summary(parameter='ohlc_window_seconds')['valueCurrent'])
        product_id = experiment.get_parameters_summary(parameter='product_id')['valueCurrent']
        prediction_horizon_steps = int(experiment.get_parameters_summary(parameter='prediction_horizon_steps')['valueCurrent'])
        history_horizon_steps = int(experiment.get_parameters_summary(parameter='history_horizon_steps')['valueCurrent'])
        
        feature_view_params = experiment.get_asset_by_name('feature_view_params.json', return_type='json')
        fv_config = FeatureViewConfig.from_params(feature_view_params)
        
        # download model artifact
        experiment.download_model(name='XBT_EUR_direction_predictor', output_path='.')
        import pickle
        with open('./inference_pipeline.pkl', 'rb') as f:
            model = pickle.load(f)
        # TODO: add wrapper around CometML to simplify this - END
        
        return cls(
            model=model,
            ohlc_window_seconds=ohlc_window_seconds,
            product_id=product_id,
            history_horizon_steps=history_horizon_steps,
            prediction_horizon_steps=prediction_horizon_steps,
            feature_view_config=fv_config,
        )


    # def _load_pickle(self, local_pickle_path):
    #     with open(local_pickle_path, 'rb') as f:
    #         model = pickle.load(f)
    #     return model
    
    def _get_defaults_ts_ms(self) -> int:
        """
        Returns ts_ms as the
        - closest timestamp to the current time
        - rounded to the nearest ohlc_window_seconds
        """
        # current UTC time
        now = datetime.now(pytz.utc)
        logger.info(f'Current UTC time: {now.strftime("%Y-%m-%d %H:%M:%S")}')

        # ts_ms as closest timestamp rouned to nearest ohlc_window_seconds
        current_sec = int(now.timestamp())
        round_sec = current_sec - (current_sec % self.ohlc_window_seconds)
        ts_ms = round_sec * 1000
        logger.info(f'{ts_ms=}')

        # log dates just for debugging purposes
        ts_datetime = datetime.utcfromtimestamp(ts_ms / 1000)
        logger.info(f'ts_datetime: {ts_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
        
        return ts_ms

    def predict(
        self,
        ts_ms: Optional[int] = None
    ) -> dict:
        """
        Predicts the target for the given timestamp `ts_ms`
        """
        if ts_ms is None:
            logger.info('No ts_ms provided, using current time to predict')
            ts_ms = self._get_defaults_ts_ms()

        # TODO: implement error handling so the API can send a proper response
        ts_data = self._read_ohlc_data_from_online_store(ts_ms)

        # timestamps = ts_data['timestamp'].values
        # close_prices = ts_data['close'].values

        # breakpoint()

        # TODO: feature engineering should be part of the
        # model pipeline, so the following block will be
        # self.model.predict(ts_data). And that is it.
        # ts_data = add_momentum_indicators(ts_data)
        # ts_data = add_volatility_indicators(ts_data)
        # features = [
        #     # raw features
        #     'close',
        #     'volume',

        #     # momentum indicators
        #     'RSI',
        #     'MACD',
        #     'MACD_Signal',
        #     'Momentum',

        #     # volatility indicators
        #     'ATR',
        #     'STD',
        # ]
        # ts_data = ts_data[features]
        predicted_prices = self.model.predict(ts_data)
        
        # combine predictions with timestamps
        # predictions = pd.DataFrame({
        #     'current_timestamp': timestamps,
        #     'current_price': close_prices,
        #     'predicted_timestamp': timestamps + self.prediction_horizon_steps * self.ohlc_window_seconds * 1000,
        #     'predicted_price': predicted_prices,
        # }).tail(5)

        response = {
            'timestamp': ts_ms + self.prediction_horizon_steps * self.ohlc_window_seconds * 1000,
            'product_id': self.product_id,
            'price': predicted_prices[-1],
        }

        logger.info(f'Response: {response}')
        # logger.info(predictions)
        
        return response
    
    def _read_ohlc_data_from_online_store(
        self,
        ts_ms: int,    
    ) -> pd.DataFrame:
        """
        Reads OHLC data from the online feature store.
        """
        # compute primary keys we need to fetch from the online feature group
        primary_keys_to_read = self._generate_list_primary_keys(ts_ms)
        logger.info(f'Reading {len(primary_keys_to_read)} primary keys from {self.feature_view_config}')
        
        # self.feature_view._fv.get_feature_vectors(entry=primary_keys_to_read, return_type="pandas")
        # breakpoint()

        # fetch data from the feature group
        ts_data : pd.DataFrame = self.feature_view.read(primary_keys_to_read)

        # Log first and last timestamp in the ts_data to spot missing data problems
        # first timestamp in the data
        first_timestamp = ts_data['timestamp'].values[0]
        first_datetime = datetime.utcfromtimestamp(first_timestamp / 1000).astimezone(timezone.utc)
        logger.info(f'First timestamp in the ts_data: {first_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
        # last timestamp
        last_timestamp = ts_data['timestamp'].values[-1]
        last_datetime = datetime.utcfromtimestamp(last_timestamp / 1000).astimezone(timezone.utc)
        logger.info(f'Last timestamp in the ts_data: {last_datetime.strftime("%Y-%m-%d %H:%M:%S")}')

        # make sure we fetched the first and last timestamp
        # it might still happen there is missing data in between, due to low volume
        # but this is something we fix during pre-processing
        # assert first_timestamp == primary_keys_to_read[0]['timestamp'], f'{first_timestamp=} != {primary_keys_to_read[0]["timestamp"]=}'
        # assert last_timestamp == primary_keys_to_read[-1]['timestamp'], f'{last_timestamp=} != {primary_keys_to_read[-1]["timestamp"]=}'

        # TODO: add error handling here if start or end timestamps are missing
        

        # # Is there any missing data in between?
        # if len(ts_data) != len(primary_keys_to_read):
        #     logger.info(f'{len(ts_data)=}')
        #     logger.info(f'{len(primary_keys_to_read)=}')
        #     logger.info('There is missing data in the feature group')
        #     # assert len(ts_data) == len(primary_keys_to_read), f'{len(ts_data)=} != {len(primary_keys_to_read)=}'
        
        return ts_data

    def _generate_list_primary_keys(
        self,
        ts_ms: int,
    ) -> List[Dict[str, Any]]:

        # to_unix_ms = ts_ms + 1000
        # from_unix_ms = to_unix_ms - (1000 * self.history_horizon_steps * self.ohlc_window_seconds)
        steps_back = self.history_horizon_steps - 1
        from_unix_ms = ts_ms - (1000 * steps_back * self.ohlc_window_seconds)
        to_unix_ms = ts_ms

        logger.info(f'Primary keys from {from_unix_ms=} to {to_unix_ms=}')
        primary_keys = []

        for unix_ms in range(from_unix_ms,
                             to_unix_ms + 1000 * self.ohlc_window_seconds,
                             1000 * self.ohlc_window_seconds):
            primary_keys.append({
                'timestamp': unix_ms,
                'product_id': self.product_id,
            })

        return primary_keys


if __name__ == '__main__':

    from rtml_tools.logging import initialize_logger
    initialize_logger()

    from argparse import ArgumentParser
    # 2 input arguments
    # - experiment_id: Optional[str]
    # - ts_ms: Optional[int]
    parser = ArgumentParser()
    parser.add_argument('--experiment_key', type=str, default=None)
    parser.add_argument('--ts_ms', type=int, default=None)
    args = parser.parse_args()

    if args.experiment_key:
        logger.info(f'Loading model from experiment_id: {args.experiment_key}')
        predictor = Predictor.from_experiment_key(args.experiment_key)
    else:
        logger.info('Loading model from local pickle')
        predictor = Predictor.from_local_pickle('model.pkl')

    predictor.predict(args.ts_ms)

    