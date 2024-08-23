import pandas as pd
import numpy as np


def load_dataset():
    benin = pd.read_csv('../data/benin-malanville.csv')   
    sierra = pd.read_csv('../data/sierraleone-bumbuna.csv')
    togo = pd.read_csv('../data/togo-dapaong_qc.csv')

    return benin, sierra, togo


def detect_outliers(data: pd.DataFrame):
    outliers = {}

    numeric_col = ['ModA', 'ModB', 'WS', 'WSgust']
    threshold = 3
    
    for col in numeric_col:
        mean = np.mean(data[col])
        std = np.std(data[col])

        z_scores = (data[col] - mean) / std
        
        outlier_data = data[col][np.abs(z_scores) > threshold].tolist()
        outliers[col] = outlier_data

    return outliers


def RH_effech_on_temp_solar(data):
    relevant_columns = ['RH', 'Tamb', 'TModA', 'GHI', 'DNI', 'DHI']
    correlation_matrix = data[relevant_columns].corr()
    return correlation_matrix['RH']