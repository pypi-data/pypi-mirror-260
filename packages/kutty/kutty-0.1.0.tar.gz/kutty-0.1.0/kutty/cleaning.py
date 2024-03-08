# Advanced code for the cleaning module
from scipy import stats
import numpy as np
import pandas as pd

# Enhanced function for handling missing values
def handle_missing_values_advanced(df, strategy='mean', columns=None):
    if columns is None:
        columns = df.columns
    if strategy == 'mean':
        df[columns] = df[columns].fillna(df[columns].mean())
    elif strategy == 'median':
        df[columns] = df[columns].fillna(df[columns].median())
    elif strategy == 'mode':
        for column in columns:
            df[column] = df[column].fillna(df[column].mode()[0])
    elif strategy == 'drop':
        df.dropna(subset=columns, inplace=True)
    else:
        raise ValueError('Invalid strategy provided.')
    return df

# Adding a new function for outlier detection and treatment
def detect_and_treat_outliers(df, columns=None, method='z_score', threshold=3):
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    if method == 'z_score':
        for column in columns:
            z_scores = np.abs(stats.zscore(df[column]))
            df = df[(z_scores < threshold)]
    elif method == 'iqr':
        for column in columns:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            df = df[(df[column] >= Q1 - 1.5 * IQR) & (df[column] <= Q3 + 1.5 * IQR)]
    else:
        raise ValueError('Invalid outlier detection method.')
    return df
