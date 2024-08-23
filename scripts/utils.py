import pandas as pd


def load_dataset():
    benin = pd.read_csv('../data/benin-malanville.csv')   
    sierra = pd.read_csv('../data/sierraleone-bumbuna.csv')
    togo = pd.read_csv('../data/togo-dapaong_qc.csv')

    return benin, sierra, togo