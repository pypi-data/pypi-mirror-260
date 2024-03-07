from typing import Optional, Union, Tuple
from datetime import datetime
import os
import logging
from pathlib import Path

import pandas as pd

from rtml_tools.feature_store_api.api import FeatureStore
from rtml_tools.feature_store_api.types import FeatureViewConfig
from rtml_tools.config import YamlConfig

logger = logging.getLogger()

def _get_cache_file_name(
    from_date: datetime,
    to_date: datetime,
    product_id: str,
) -> str:
    """Returns the name of the cache file for the given parameters."""
    return f"{product_id.replace('/', '-')}_{from_date}_{to_date}.parquet"

def _load_ohlc_data_from_cache(
    from_date: datetime,
    to_date: datetime,
    product_id: str,
    cache_dir: str,
) -> Union[pd.DataFrame, None]:
    """Loads OHLC data from local Parquet file in the `cache_dir`."""
    file_path = Path(cache_dir) / _get_cache_file_name(from_date, to_date, product_id)

    try:
        ts_data = pd.read_parquet(file_path)
        logger.info(f'Successfully loaded OHLC data from cache file {file_path}')
        return ts_data
    except FileNotFoundError:
        logger.info(f'File {file_path} not found in local cache')
        pass
    except Exception as e:
        logger.info(f"Failed to read data from existing cache file {file_path}")
        pass
    
    return None

def _save_ohlc_data_to_cache(
    ts_data: pd.DataFrame,
    from_date: datetime,
    to_date: datetime,
    product_id: str,
    cache_dir: str,
) -> None:
    """Saves OHLC data to local Parquet file in the `cache_dir`."""
    # make sure the cache_dir exists
    Path(cache_dir).mkdir(parents=True, exist_ok=True)

    file_path = Path(cache_dir) / _get_cache_file_name(from_date, to_date, product_id)

    # breakpoint()

    ts_data.to_parquet(file_path)
    logger.info(f'Successfully saved OHLC data to cache file {file_path}')


def get_ohlc_data_from_store(
    from_date: datetime,
    to_date: datetime,
    product_id: str,
    feature_view_params: dict,
    # global_config: YamlConfig,
    cache_dir: Optional[str] = None,
) -> pd.DataFrame:
    """"""
    if cache_dir is not None:
        # try to load data from local cache
        ts_data = _load_ohlc_data_from_cache(from_date, to_date, product_id, cache_dir)
        if ts_data is not None:
            # if we have successfully loaded the data from cache, return it
            return ts_data
        
    # connect to the feature store
    feature_store = FeatureStore(
        api_key=os.environ["HOPSWORKS_API_KEY"],
        project_name=os.environ["HOPSWORKS_PROJECT_NAME"],
    )

    # and read a batch of data from the offline feature store
    fv_config = FeatureViewConfig.from_params(feature_view_params)
    fv = feature_store.get_or_create_feature_view(fv_config)
    ts_data = fv.read_offline(from_date, to_date)
    # ts_data = fv._fv.get_batch_data()
    # from_ms = int(from_date.timestamp() * 1000)
    # to_ms = int(to_date.timestamp() * 1000)
    # ts_data = ts_data[ts_data.timestamp.between(from_ms, to_ms)]
    
    # keep only the data for the given product_id
    ts_data = ts_data[ts_data['product_id'] == product_id]
    # and sort by timestamp
    ts_data = ts_data.sort_values('timestamp')

    # log the max and min timestamp in ts_data expressed
    # as datetime, to compare them with from_date and to_date
    min_ts = ts_data['timestamp'].min()
    max_ts = ts_data['timestamp'].max()
    logger.info(f"min timestamp: {datetime.fromtimestamp(min_ts / 1000)}")
    logger.info(f"max timestamp: {datetime.fromtimestamp(max_ts / 1000)}")
    
    if cache_dir is not None:
        # save data to local cache
        _save_ohlc_data_to_cache(ts_data, from_date, to_date, product_id, cache_dir)

    return ts_data

def add_perc_change_column(
    ts_data: pd.DataFrame,
    window_size: Optional[int] = 1,
    drop_nans: Optional[bool] = True,
) -> pd.DataFrame:
    """
    Adds a target column to the OHLC data.

    The target column is the value of the 'close' column at the end of the
    window of size `window_size` following each row in the OHLC data.

    The target column is named `target_column` and is added to the OHLC data.

    Args:
        ts_data (pd.DataFrame): The OHLC data.
        target_column (str): The name of the target column to add.
        window_size (int): The size of the window to use to compute the target.

    Returns:
        pd.DataFrame: The OHLC data with the target column added.
    """
    next_price = ts_data['close'].shift((-1)*window_size)
    
    ts_data['perc_change'] = (next_price - ts_data['close']) / ts_data['close']
    
    if drop_nans:
        # drop rows with NaN values in the perc_change column
        ts_data.dropna(subset=['perc_change'], inplace=True)

    return ts_data

def get_perc_change_terciles(
    ts_data: pd.DataFrame,
) -> Tuple[float, float]:
    """
    Terceles are the two values that split the data into 3 equally sized parts.
    """
    terciles = ts_data['perc_change'].quantile([1./3, 2./3])
    return terciles.values[0], terciles.values[1]

def add_discrete_target_column(
    ts_data: pd.DataFrame,
    threshold_1: float,
    threshold_2: float,
) -> pd.DataFrame:
    """
    """
    def cont2discrete(x: float) -> int:
        if x < threshold_1:
            return -1
        elif x < threshold_2:
            return 0
        else:
            return 1
    
    ts_data['target'] = ts_data['perc_change'].apply(cont2discrete)
    
    return ts_data


if __name__ == '__main__':

    get_ohlc_data_from_store(
        from_date=datetime(2023, 1, 6),
        to_date=datetime(2025, 2, 5),
        cache_dir='./.cache/ohlc_data/'
    )

