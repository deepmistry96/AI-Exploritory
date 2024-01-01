import requests
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
import pandas as pd

ALPHAVANTAGE_API_KEY = "2JW0VYC6INQB3DD7"

def get_hourly_prices(ticker):
    ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')

    if data is not None:
        return data['4. close'].tolist()
    else:
        return []

def prepare_data_for_lstm(prices, time_steps=60):
    # Convert to a numpy array
    prices = np.array(prices).reshape(-1, 1)

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    # Create sequences
    X, y = [], []
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])  # Predict the next time step

    return np.array(X), np.array(y)

def save_original_prices_data(prices, time_steps=60, filename="original_prices.csv"):
    df = pd.DataFrame({'Original_Prices': prices})
    df_shifted = df.shift(-time_steps)
    df_combined = pd.concat([df, df_shifted], axis=1)
    df_combined.columns = ['Current_Price', 'Next_Price']
    df_combined.dropna(inplace=True)
    df_combined.to_csv(filename, index=False)
    print(f"Original prices data saved to {filename}")

def save_lstm_data(X, y, filename):
    # Combine X and y for saving
    df_X = pd.DataFrame([x.flatten() for x in X])
    df_y = pd.DataFrame(y, columns=["target"])
    df = pd.concat([df_X, df_y], axis=1)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    ticker = input("Enter a stock ticker: ")

    hourly_prices = get_hourly_prices(ticker)

    if hourly_prices:
        print(f"Fetched {len(hourly_prices)} price points.")
        print("Sample prices:", hourly_prices[:5])

        X, y = prepare_data_for_lstm(hourly_prices, time_steps=60)
        original_prices_filename = f"{ticker}_hourly_prices.csv"

        if X.size > 0 and y.size > 0:
            print("Data prepared for LSTM.")
            lstm_filename = f"{ticker}_lstm_data.csv"
            save_lstm_data(X, y, lstm_filename)
            save_original_prices_data(hourly_prices, time_steps=60, filename=original_prices_filename)
        else:
            print("Failed to prepare data for LSTM.")
    else:
        print("No data fetched. Please check the ticker symbol or API limitations.")
