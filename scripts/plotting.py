import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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


def corr_analysis(data: pd.DataFrame):

    solar_columns = ['GHI', 'DHI', 'DNI']
    temperature_columns = ['TModA', 'TModB']

    corr_columns = data[solar_columns + temperature_columns]
    correlation_matrix = corr_columns.corr()

    plt.figure(figsize=(12,8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Analysis')
    plt.show()
    

def corr_wind_solar(data):
    wind_col = ['WS', 'WSgust', 'WD']
    solar_col = ['GHI', 'DNI', 'DHI']

    fig, axes = plt.subplots(ncols=3, nrows=3, figsize=(12, 10))

    for i, wind in enumerate(wind_col):
        for j, solar in enumerate(solar_col):
            sns.scatterplot(x=data[wind], y=data[solar], ax=axes[i, j])
            axes[i, j].set_title(f'{wind} vs {solar}')
            axes[i, j].tick_params(axis='x', rotation=45)
            axes[i, j].set_xlabel(wind)
            axes[i, j].set_ylabel(solar)


    plt.suptitle("Scatter Matrix: Wind Conditions and Solar Irradiance")
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.show()



def freq_histograms(data: pd.DataFrame):

    cols = ['GHI', 'DNI', 'DHI', 'WS', 'TModA', 'TModB', 'Tamb']

    num_rows = 3
    num_cols = 3

    fig, axes = plt.subplots(ncols= num_cols, nrows=num_rows, figsize=(12,10))

    for i, col in enumerate(cols):
        row = i // 3
        col_idx = i % 3

        axes[row, col_idx].hist(data[col], bins=20, edgecolor='white')
        axes[row, col_idx].set_xlabel(col)
        axes[row, col_idx].set_ylabel('Frequency')

    # Remove empty subplots if there are any
    for i in range(len(cols), num_rows * num_cols):
        fig.delaxes(axes.flatten()[i])

    plt.tight_layout(pad=2.0)
    plt.show()


def bubble_charts(data):

    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(data['GHI'], data['Tamb'], s=data['RH'], c=data['BP'], cmap='viridis', alpha=0.6, edgecolors='w', linewidth=0.5)

    cbar = plt.colorbar(scatter)
    cbar.set_label('Barometric Pressure (BP)')

    plt.xlabel('Global Horizontal Irradiance (GHI) [W/m²]')
    plt.ylabel('Ambient Temperature (Tamb) [°C]')
    plt.title('Bubble Chart: GHI vs. Tamb with Bubble Size Representing RH and Color Representing BP')

    plt.show()    