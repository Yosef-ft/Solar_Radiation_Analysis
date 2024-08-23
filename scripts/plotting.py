import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def data_grouper(data: pd.DataFrame) -> tuple:
    '''
    This function groups timeseries data by day, months and year

    Returns:
        tuple: A tuple containing three DataFrames - grouped by day, month, and year.
    '''

    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data.index = data['Timestamp']

    day_data = data.groupby([data.index.month, data.index.day, data.index.year])[['GHI', 'DNI', 'DHI', 'Tamb']].mean()
    month_data = data.groupby([data.index.month, data.index.year])[['GHI', 'DNI', 'DHI', 'Tamb']].mean()
    year_data = data.groupby([data.index.year])[['GHI', 'DNI', 'DHI', 'Tamb']].mean()

    return day_data, month_data, year_data



def plot_timeseries(data):

    day_data, month_data, year_data = data_grouper(data)
    day_data['Date'] = day_data.index.to_series().apply(lambda idx: pd.Timestamp(year=idx[2], month=idx[0], day=idx[1]).date())

    # plot for day data 
    fig, axes = plt.subplots(nrows=4, figsize=(10, 12))
    cols = ['GHI', 'DNI', 'DHI', 'Tamb']
    plt.suptitle('Day Data', fontsize = 16)
    for i, col in enumerate(cols):
        axes[i].plot(day_data['Date'], day_data[col])
        axes[i].set_ylabel(col)
        axes[i].tick_params(axis='x', rotation=45)

    plt.xlabel('Timestamp')
    plt.tight_layout()
    plt.show()

    # plot for month data
    fig, axes = plt.subplots(nrows=4, figsize=(10, 12))
    cols = ['GHI', 'DNI', 'DHI', 'Tamb']
    plt.suptitle('Month Data', fontsize = 16)
    for i, col in enumerate(cols):
        month_data[col].plot(ax = axes[i])
        axes[i].set_ylabel(col)
        axes[i].tick_params(axis='x', rotation=45)

    plt.xlabel('Timestamp')
    plt.tight_layout()
    plt.show()    

    # plot for year data
    fig, axes = plt.subplots(nrows=4, figsize=(10, 12), )
    cols = ['GHI', 'DNI', 'DHI', 'Tamb']
    plt.suptitle('Year Data', fontsize = 16)
    for i, col in enumerate(cols):
        year_data[col].plot(ax = axes[i])
        axes[i].set_ylabel(col)
        axes[i].tick_params(axis='x', rotation=45)

    plt.xlabel('Timestamp')
    plt.tight_layout()
    plt.show()    


def cleaning_impact(data: pd.DataFrame):
    clean_data = data[data['Cleaning'] == 1]
    unclean_data = data[data['Cleaning'] == 0]

    mean_cleaned = clean_data[['ModA', 'ModB', 'WS', 'WSgust']].mean()
    mean_uncleaned = unclean_data[['ModA', 'ModB', 'WS', 'WSgust']].mean()

    # If impact_A and impact_B are significantly positive, it indicates that cleaning likely improved the sensor readings.
    impact_A = mean_cleaned['ModA'] - mean_uncleaned['ModA']
    impact_B = mean_cleaned['ModB'] - mean_uncleaned['ModB']   
    impact_WS = mean_cleaned['WS'] - mean_uncleaned['WS']
    impact_WSgust = mean_cleaned['WSgust'] - mean_uncleaned['WSgust'] 

    # Plot time series for ModA
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['ModA'], label='ModA', color='blue', alpha=0.5)
    plt.scatter(clean_data.index, clean_data['ModA'], label='Cleaning Event (ModA)', color='red')
    plt.title('Impact of Cleaning on ModA Over Time')
    plt.xlabel('Time')
    plt.ylabel('ModA (W/m²)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot time series for ModB
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['ModB'], label='ModB', color='green', alpha=0.5)
    plt.scatter(clean_data.index, clean_data['ModB'], label='Cleaning Event (ModB)', color='red')
    plt.title('Impact of Cleaning on ModB Over Time')
    plt.xlabel('Time')
    plt.ylabel('ModB (W/m²)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot time series for WS
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['WS'], label='WS', color='orange', alpha=0.7)
    plt.scatter(clean_data.index, clean_data['WS'], label='Cleaning Event (WS)', color='red')
    plt.title('Impact of Cleaning on Wind Speed (WS) Over Time')
    plt.xlabel('Time')
    plt.ylabel('WS (m/s)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot time series for WSgust
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['WSgust'], label='WSgust', color='purple', alpha=0.7)
    plt.scatter(clean_data.index, clean_data['WSgust'], label='Cleaning Event (WSgust)', color='red')
    plt.title('Impact of Cleaning on Wind Gust Speed (WSgust) Over Time')
    plt.xlabel('Time')
    plt.ylabel('WSgust (m/s)')
    plt.legend()
    plt.grid(True)
    plt.show()

    return impact_A, impact_B, impact_WS, impact_WSgust