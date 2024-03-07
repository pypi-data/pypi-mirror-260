from typing import Tuple, Optional

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class MissingValuesFiller(BaseEstimator, TransformerMixin):
    """
    Adds missing timestamps to the dataset, and fills
    - missing prices with forward and back filling
    - missing volume with 0
    """
    def __init__(
        self,
        step_ms: Optional[int] = 60000
    ):
        self.step_ms = step_ms

    def _fill_missing_timestamps(
        self,
        ts_data: pd.DataFrame,
        # step_ms: int,
    ) -> pd.DataFrame:
        """
        Fills missing close prices by 
        - forward filling, and
        - back filling
        """
        df = ts_data.copy()

        # select only the relevant columns
        df = df[['timestamp', 'high', 'low', 'close', 'volume']]

        # expand the index to include all timestamps
        df = df.set_index('timestamp')
        from_ts_ms = ts_data['timestamp'].min()
        to_ts_ms = ts_data['timestamp'].max()
        df = df.reindex(range(from_ts_ms, to_ts_ms + self.step_ms, self.step_ms))

        # fill in missing prices with forward and back filling
        df['high'] = df['high'].ffill()
        df['high'] = df['high'].bfill()
        df['low'] = df['low'].ffill()
        df['low'] = df['low'].bfill()
        df['close'] = df['close'].ffill()
        df['close'] = df['close'].bfill()

        # fill in missing volume with 0
        df['volume'] = df['volume'].fillna(0)

        # reset index
        df = df.reset_index()

        return df

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return self._fill_missing_timestamps(X)
    
    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)
    

class TargetColumnAdder(BaseEstimator, TransformerMixin):
    """
    Adds a discrete target column to the dataset, with values
        -1 -> when price decreases more than `tercile_1`
        0  -> when price is between `tercile_1` and `tercile_2`
        +1 -> when price increases more than `tercile_2`
    """
    def __init__(
        self,
        window_size: Optional[int] = 1
    ):
        self.window_size = window_size
        self.tercile_1 = None
        self.tercile_2 = None

    def _get_perc_change_terciles(self, X) -> Tuple[float, float]:
        """
        Compute the terciles of the price percentage change
        """
        # ts_data = X.copy()

        perc_change = self._get_percentage_change(X)
        terciles = perc_change.quantile([1./3, 2./3])

        return terciles.values[0], terciles.values[1]

    def _get_percentage_change(self, X) -> pd.Series:

        next_price = X['close'].shift((-1)*self.window_size)
        perc_change = (next_price - X['close']) / X['close']

        return perc_change
    
    def _cont2discrete(self, x: float) -> int:
        if x < self.tercile_1:
            return -1
        elif x > self.tercile_2:
            return 1
        else:
            return 0
        
    def fit(self, X, y=None):
    
        self.tercile_1, self.tercile_2 = self._get_perc_change_terciles(X)
        
        return self

    def transform(self, X, y=None):
        
        X_ = X.copy()

        perc_change : pd.Series = self._get_percentage_change(X_)
        X_['target'] = perc_change.apply(self._cont2discrete)

        return X_
    
    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)


