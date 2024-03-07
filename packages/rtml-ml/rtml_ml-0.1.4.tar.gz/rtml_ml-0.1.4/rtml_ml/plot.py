from typing import Optional

import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, Figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter, DatetimeTickFormatter
from bokeh.io import output_notebook
from bokeh.transform import factor_cmap
from datetime import datetime, timedelta


def plot_ohlc(
    ts_data: pd.DataFrame,
    color_column: Optional[str] = None
) -> Figure:
    
    df = pd.DataFrame(ts_data)

    # Convert timestamp to UTC datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)

    # Calculate candle width based on time difference
    time_diff = (df['timestamp'].iloc[1] - df['timestamp'].iloc[0]).total_seconds() * 1000  # in milliseconds
    candle_width = time_diff * 0.7  # Adjust the multiplier to control the width

    # Determine the direction of movement (increase or decrease)
    df['direction'] = ['increase' if close > open_ else 'decrease' for open_, close in zip(df['open'], df['close'])]

    # Map direction to colors
    colors = {'increase': 'green', 'decrease': 'red'}
    df['color'] = df['direction'].map(colors)

    # Create a ColumnDataSource
    source = ColumnDataSource(df)

    # Create a figure
    p = figure(x_axis_type='datetime', title='OHLC Data', plot_width=800, plot_height=400)

    # Plot OHLC data with different colors for increase and decrease
    p.segment(x0='timestamp', y0='low', x1='timestamp', y1='high', color='black', source=source)
    p.vbar(x='timestamp', width=candle_width, top='open', bottom='close', fill_color=factor_cmap('direction', palette=['green', 'red'], factors=['increase', 'decrease']), line_color='black', source=source)

    # Add axes labels and format ticks
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.xaxis.formatter = DatetimeTickFormatter(days="%m/%d", hours="%H:%M", seconds="%Ss", milliseconds="%3Nms")
    p.yaxis.formatter = NumeralTickFormatter(format='0.00')

    # Show the plot
    output_notebook()
    show(p)

    # breakpoint()

    return p

def plot_histogram_perc_change(
    ts_data: pd.DataFrame,
    percentile: Optional[float] = None
) -> Figure:
    
    df = ts_data

    if percentile is not None:
        assert 0 <= percentile <= 1, 'percentile must be between 0 and 1'
        max_perc = df['perc_change'].quantile(percentile)
        min_perc = df['perc_change'].quantile(1 - percentile)

        # Filter the data
        df = df[df['perc_change'] <= max_perc]
        df = df[df['perc_change'] >= min_perc]

    # Creating a histogram
    hist, edges = np.histogram(df['perc_change'], bins=200)

    # Creating the figure
    p = figure(title='Percentage Change Histogram', background_fill_color='#f0f0f0')

    # Adding a quad glyph
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color='navy', line_color='white', alpha=0.5)

    # Formatting the y-axis to show percentage
    p.yaxis.formatter = NumeralTickFormatter(format='0.0%')

    # Show the plot
    output_notebook()
    show(p)

    return p

