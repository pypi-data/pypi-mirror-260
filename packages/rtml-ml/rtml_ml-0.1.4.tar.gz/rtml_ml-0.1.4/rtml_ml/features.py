from typing import Optional, List

import pandas as pd
import talib
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import FunctionTransformer


def get_feature_engineering_pipeline(
    rsi_timeperiod: Optional[int] = 14,
    macd_fastperiod: Optional[int] = 12,
    macd_slowperiod: Optional[int] = 26,
    macd_signalperiod: Optional[int] = 9,
    momentum_timeperiod: Optional[int] = 10,
    atr_timeperiod: Optional[int] = 14,
    std_timeperiod: Optional[int] = 20,
) -> Pipeline:
    """
    Returns scikit-learn pipeline for feature engineering
    """
    # momentum indicators
    RSI = FunctionTransformer(
        add_rsi_indicator,
        kw_args={'timeperiod': rsi_timeperiod})
    
    MACD = FunctionTransformer(
        add_macd_indicator,
        kw_args={'fastperiod': macd_fastperiod,
                 'slowperiod': macd_slowperiod,
                 'signalperiod': macd_signalperiod})
    
    Momentum = FunctionTransformer(
        add_momentum_indicator,
        kw_args={'timeperiod': momentum_timeperiod})
    
    # volatility indicators
    AverageTrueRange = FunctionTransformer(
        add_average_true_range,
        kw_args={'timeperiod': atr_timeperiod})
    
    STD = FunctionTransformer(
        add_std,
        kw_args={'timeperiod': std_timeperiod})

    return make_pipeline(
        RSI,
        MACD,
        Momentum,
        AverageTrueRange,
        STD,
    )


def add_rsi_indicator(
    ts_data: pd.DataFrame,
    timeperiod: Optional[int] = 14
) -> pd.DataFrame:
    """
    Adds the RSI (Relative Strength Index) indicator to the `ts_data`
    """
    ts_data['RSI'] = talib.RSI(ts_data['close'], timeperiod=timeperiod)
    return ts_data


def add_macd_indicator(
    ts_data: pd.DataFrame,
    fastperiod: Optional[int] = 12,
    slowperiod: Optional[int] = 26,
    signalperiod: Optional[int] = 9,
) -> pd.DataFrame:
    """
    Adds the MACD (Moving Average Convergence Divergence) indicator to the `ts_data`
    """
    macd, macd_signal, _ = talib.MACD(ts_data['close'],
                                      fastperiod=fastperiod,
                                      slowperiod=slowperiod,
                                      signalperiod=signalperiod)
    ts_data['MACD'] = macd
    ts_data['MACD_Signal'] = macd_signal
    return ts_data


def add_momentum_indicator(
    ts_data: pd.DataFrame,
    timeperiod: Optional[int] = 10,
) -> pd.DataFrame:
    """
    Adds the RSI (Relative Strength Index) and MACD (Moving Average Convergence Divergence) indicators to the `ts_data`
    """
    ts_data['Momentum'] = talib.MOM(ts_data['close'], timeperiod=timeperiod)
    return ts_data


def add_average_true_range(
    ts_data: pd.DataFrame,
    timeperiod: Optional[int] = 14
) -> pd.DataFrame:
    """
    Adds the ATR (Average True Range) indicator to the `ts_data`
    """
    ts_data['ATR'] = talib.ATR(ts_data['high'],
                               ts_data['low'],
                               ts_data['close'],
                               timeperiod=timeperiod)
    return ts_data


def add_std(
    ts_data: pd.DataFrame,
    timeperiod: Optional[int] = 20
) -> pd.DataFrame:
    """
    Adds the STD (Standard Deviation) indicator to the `ts_data`
    """
    ts_data['STD'] = talib.STDDEV(ts_data['close'], timeperiod=timeperiod)
    return ts_data