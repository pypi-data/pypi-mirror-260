# Advanced code for the time series module
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

# Enhanced moving average function with support for simple, weighted, and exponential moving averages
def calculate_moving_average(series, window, type='simple'):
    if type == 'simple':
        return series.rolling(window=window).mean()
    elif type == 'weighted':
        weights = np.arange(1, window + 1)
        return series.rolling(window=window).apply(lambda x: np.dot(x, weights)/weights.sum(), raw=True)
    elif type == 'exponential':
        return series.ewm(span=window, adjust=False).mean()
    else:
        raise ValueError('Invalid type provided.')

# New function for anomaly detection in time series data
# Simple statistical approach: outliers are points outside 1.5 * IQR in the residual component after seasonal decomposition
def detect_anomalies(series, window=12):
    decomposed = seasonal_decompose(series, model='additive', period=window)
    residual = decomposed.resid.dropna()
    q1, q3 = np.percentile(residual, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    anomalies = residual[(residual < lower_bound) | (residual > upper_bound)]
    return anomalies.index

