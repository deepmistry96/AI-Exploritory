import requests
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split

ALPHAVANTAGE_API_KEY = "2JW0VYC6INQB3DD7"
ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')

def get_hourly_prices(ticker):
    data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    if data is not None:
        return data['4. close'].tolist()
    else:
        return []

def prepare_data_for_lstm(prices, time_steps=60):
    prices = np.array(prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])
    
    return np.array(X), np.array(y), scaler

ticker = input("Enter a stock ticker: ")
hourly_prices = get_hourly_prices(ticker)

if hourly_prices:
    print(f"Fetched {len(hourly_prices)} price points.")
    X, y, scaler = prepare_data_for_lstm(hourly_prices)

    if X.size > 0 and y.size > 0:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(1)
        ])

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=50, batch_size=32)

        last_sequence = np.expand_dims(X[-1], axis=0)
        next_price_scaled = model.predict(last_sequence)
        next_price = scaler.inverse_transform(next_price_scaled.reshape(-1, 1))

        print("Next 5 minutes prediction (price):", round(next_price[0][0], 0))
    else:
        print("Not enough data to prepare for LSTM.")
else:
    print("No data fetched. Please check the ticker symbol or API limitations.")
