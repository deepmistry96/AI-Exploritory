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
symbol = input('Enter Stock Ticker Here: ')
market_open = 9.5
market_close = 16

# Function to fetch hourly prices
def fetch_hourly_prices(date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/hour/{date}/{date}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data:
            df = pd.DataFrame(json_data['results'])
            df['datetime'] = pd.to_datetime(df['t'], unit='ms')
            df = df.set_index('datetime').between_time(f'{int(market_open)}:30', f'{int(market_close)}:00')
            return df['c'].values  # Extract only closing prices
        else:
            return np.array([])
    else:
        return np.array([])

# Function to create a unique file name
def create_unique_file_name(base_name, extension, counter):
    return f"{base_name}{counter}{extension}" if counter > 0 else f"{base_name}{extension}"

# Fetch and write prices to a CSV file
start_date = datetime.now() - timedelta(days=6*30)
hourly_prices = []

while start_date < datetime.now():
    if start_date.weekday() < 5:  # Skip weekends
        date_str = start_date.strftime('%Y-%m-%d')
        daily_prices = fetch_hourly_prices(date_str)
        hourly_prices.extend(daily_prices)
    start_date += timedelta(days=1)

# Check for unique file name
base_file_name = f'{symbol}_prices'
file_extension = '.csv'
file_counter = 0

while True:
    csv_file_name = create_unique_file_name(base_file_name, file_extension, file_counter)
    if not os.path.exists(csv_file_name):
        break
    file_counter += 1

# Write prices to the CSV file
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Price'])  # Writing header
    for price in hourly_prices:
        writer.writerow([price])

print(f"Prices written to {csv_file_name}")


start_date = datetime.now() - timedelta(days=6*30)


while start_date < datetime.now():
    if start_date.weekday() < 5:  # Skip weekends
        date_str = start_date.strftime('%Y-%m-%d')
        daily_prices = fetch_hourly_prices(date_str)
        hourly_prices.extend(daily_prices)
    start_date += timedelta(days=1)

# Prepare data for LSTM
def prepare_data_for_lstm(prices, time_steps=120):
    #Tweak: Try different time steps like 30, 90, or 120.
    #This defines how many past hours the model looks at to make a prediction. A larger window might 
    #capture more trends but could also introduce noise.

    prices = np.array(prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])
    
    return np.array(X), np.array(y), scaler

if hourly_prices:
    print(f"Fetched {len(hourly_prices)} price points.")
    X, y, scaler = prepare_data_for_lstm(hourly_prices)

    if X.size > 0 and y.size > 0:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        #Tweak: Experiment with different ratios like 0.3 or 0.1.
        #A larger test set gives a better idea of how the model performs on unseen data, but reduces the data available for training.
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        # LSTM Model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            #Tweak: Try different rates like 0.1, 0.3, or 0.5.
            #Dropout prevents overfitting by randomly dropping units, but too much dropout can lead to underfitting.
            Dense(1)
            #Tweak: Experiment with more layers or different numbers of units (e.g., 100 units or 3 layers).
            #More layers/units can capture complex patterns but may also lead to overfitting.
        ])

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=50, batch_size=32)
        #Tweak: Increase or decrease (e.g., 30, 70).
        #More epochs can lead to better learning but also to overfitting.

        #Tweak: Try different sizes like 16, 64, or 128.
        #Larger batch sizes can speed up training but might impact the model's ability to generalize.

        # Calculate how many hours to predict ahead
        now = datetime.now(pytz.timezone('US/Eastern'))
        market_close_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
        if now > market_close_time:
            market_close_time += timedelta(days=1)

        hours_ahead = int((market_close_time - now).total_seconds() / 3600)
        future_steps = hours_ahead - 1  # Subtract 1 because we want the hour before market close

        # Predict next price
        if future_steps < len(X):
            last_sequence = np.expand_dims(X[-future_steps], axis=0)
        else:
            # Not enough data to predict that far ahead
            print("Not enough data to predict that far ahead.")
            last_sequence = np.expand_dims(X[-1], axis=0)  # Fallback to the last available sequence

        next_price_scaled = model.predict(last_sequence)
        next_price = scaler.inverse_transform(next_price_scaled.reshape(-1, 1))

        print("Predicted price at 4 PM:", round(next_price[0][0], 2))
    else:
        print("Not enough data")