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
    prices = np.array(prices).reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X = []
    for i in range(len(scaled_prices) - time_steps):
        X.append(scaled_prices[i:i + time_steps])

    return np.array(X)

def save_lstm_data(data, filename):
    df = pd.DataFrame([x.flatten() for x in data])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    ticker = input("Enter a stock ticker: ")

    hourly_prices = get_hourly_prices(ticker)


    if hourly_prices:
        print(f"Fetched {len(hourly_prices)} price points.")
        print("Sample prices:", hourly_prices[:5])

        lstm_ready_data = prepare_data_for_lstm(hourly_prices, time_steps=60)

        if lstm_ready_data.size > 0:
            print("Data prepared for LSTM.")
            filename = f"{ticker}_lstm_data.csv"
            save_lstm_data(lstm_ready_data, filename)
        else:
            print("Failed to prepare data for LSTM.")
    else:
        print("No data fetched. Please check the ticker symbol or API limitations.")
