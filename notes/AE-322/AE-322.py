import os
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

# Polygon API for data fetching
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

def create_unique_file_name(base_name, extension, counter):
    return f"{base_name}{counter}{extension}" if counter > 0 else f"{base_name}{extension}"

start_date = datetime.now() - timedelta(days=6*30)
hourly_prices = []

while start_date < datetime.now():
    if start_date.weekday() < 5:
        date_str = start_date.strftime('%Y-%m-%d')
        daily_prices = fetch_hourly_prices(date_str)
        hourly_prices.extend(daily_prices)
    start_date += timedelta(days=1)

base_file_name = f'{symbol}_prices'
file_extension = '.csv'
file_counter = 0

while True:
    csv_file_name = create_unique_file_name(base_file_name, file_extension, file_counter)
    if not os.path.exists(csv_file_name):
        break
    file_counter += 1

with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Price'])
    for price in hourly_prices:
        writer.writerow([price])

print(f"Prices written to {csv_file_name}")

def prepare_data_for_lstm(prices, time_steps=30):
    prices = np.array(prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])
    
    return np.array(X), np.array(y), scaler

if hourly_prices:
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

        now = datetime.now(pytz.timezone('US/Eastern'))
        market_close_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
        if now > market_close_time:
            market_close_time += timedelta(days=1)

        hours_ahead = int((market_close_time - now).total_seconds() / 3600)
        future_steps = hours_ahead - 1

        if future_steps < len(X):
            last_sequence = np.expand_dims(X[-future_steps], axis=0)
        else:
            last_sequence = np.expand_dims(X[-1], axis=0)

        next_price_scaled = model.predict(last_sequence)
        next_price = scaler.inverse_transform(next_price_scaled.reshape(-1, 1))

        print("Predicted price at 4 PM:", round(next_price[0][0], 2))
    else:
        print("Not enough data")