import io
import requests
import numpy as np
import pandas as pd
import csv
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import pytz
import tensorflow as tf

np.random.seed(42)
tf.random.set_seed(42)

POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"
symbol = "AAPL"
market_open = 9.5
market_close = 16

def fetch_hourly_prices(date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/hour/{date}/{date}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data:
            df = pd.DataFrame(json_data['results'])
            df['datetime'] = pd.to_datetime(df['t'], unit='ms')
            df = df.set_index('datetime').between_time(f'{int(market_open)}:30', f'{int(market_close)}:00')
            return df['c'].values
        else:
            return np.array([])
    else:
        return np.array([])

csv_file_name = './datasets/AMZN_2_hours_till_close.csv'

with open(csv_file_name, 'r') as file:
    lines = file.readlines()
    last_line = lines[-1]
    if not last_line[0].isdigit():
        lines = lines[:-1] 

csv_data = ''.join(lines)
df = pd.read_csv(io.StringIO(csv_data))

def prepare_data_for_lstm(prices, time_steps=120):
    prices = np.array(prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])
    
    return np.array(X), np.array(y), scaler

hourly_prices = df['Price'].to_numpy()
if hourly_prices.size > 0:
    X, y, scaler = prepare_data_for_lstm(hourly_prices)
    if X.size > 0 and y.size > 0:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
            Dropout(0.1),
            LSTM(50, return_sequences=False),
            Dropout(0.1),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=50, batch_size=32)


        hours_ahead = 5
        future_steps = int(hours_ahead * 60 / 60)  
        
        if future_steps < len(X):
            last_sequence = np.expand_dims(X[-future_steps], axis=0)
        else:
            last_sequence = np.expand_dims(X[-1], axis=0)
        next_price_scaled = model.predict(last_sequence)
        next_price = scaler.inverse_transform(next_price_scaled.reshape(-1, 1))

        print("Predicted price at 4 PM:", round(next_price[0][0], 2))
    else:
        print("Not enough data")
