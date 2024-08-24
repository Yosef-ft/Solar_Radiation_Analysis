import streamlit as st
import plotly.express as px

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')
import seaborn as sns


st.set_page_config(
    page_title="Solar Radiation Analysis",
    page_icon=":bar_chart:",
    layout="wide"
)

class Analysis:
    def __init__(self, data):
        self.data = data

    def corr_wind_solar(self):
        wind_col = ['WS', 'WSgust', 'WD']
        solar_col = ['GHI', 'DNI', 'DHI']

        fig, axes = plt.subplots(ncols=3, nrows=3, figsize=(12, 10))

        for i, wind in enumerate(wind_col):
            for j, solar in enumerate(solar_col):
                sns.scatterplot(x=self.data[wind], y=self.data[solar], ax=axes[i, j])
                axes[i, j].set_title(f'{wind} vs {solar}')
                axes[i, j].tick_params(axis='x', rotation=45)
                axes[i, j].set_xlabel(wind)
                axes[i, j].set_ylabel(solar)

        plt.suptitle("Scatter Matrix: Wind Conditions and Solar Irradiance")
        plt.subplots_adjust(wspace=0.4, hspace=0.4)
        st.pyplot(fig)  


@st.cache_data
def load_data(path: str):
    data = pd.read_csv(path)
    return data

upload_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "pdf"])

if upload_file is None:
    st.info("Upload a file to proceed.", icon="ℹ️")
    st.stop()


df = load_data(upload_file)

an = Analysis(df)
an.corr_wind_solar()