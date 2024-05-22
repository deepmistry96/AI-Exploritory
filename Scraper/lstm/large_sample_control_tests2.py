import os
import numpy as np
import pandas as pd
import csv
import requests
from datetime import datetime
from pytz import timezone
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Configuration
POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"
central = timezone('US/Central')
time_steps = 120

# Function to fetch 5-minute prices and calculate the average
def fetch_5min_prices(symbol, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/minute/{date}/{date}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data and len(json_data['results']) > 0:
            df = pd.DataFrame(json_data['results'])
            df['datetime'] = pd.to_datetime(df['t'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(central)
            df = df.set_index('datetime').between_time('10:00', '16:00')
            return df['c'].mean()
        else:
            print(f"No data returned for {symbol} on {date}.")
            return None
    else:
        print(f"Failed to fetch prices for {symbol} on {date}. Status Code: {response.status_code}, Error: {response.text}")
        return None
    


# Function to prepare data for LSTM
def prepare_data_for_lstm(prices, time_steps=120):
    prices = np.array(prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])
    return np.array(X), np.array(y), scaler
def create_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def perform_prediction_runs(X, y, scaler):
    all_predictions = []
    # Initialize a new model inside the loop to ensure it starts fresh for each run
    for run in range(8):  # Considers performing 8 runs
        model = create_model((X.shape[1], 1))
        model.fit(X, y, epochs=50, batch_size=32, verbose=0)

        hourly_predictions = []
        last_sequence = X[-1].reshape((1, X.shape[1], 1))  # Prepare the last sequence from the actual data
        for hour_ahead in range(1, 6):  # Predict 1-5 hours ahead
            current_prediction = model.predict(last_sequence)
            predicted_value = scaler.inverse_transform(current_prediction)[0][0]
            hourly_predictions.append(predicted_value)
            # Prepare the last sequence for the next prediction
            last_sequence = np.roll(last_sequence, -1)
            last_sequence[0, -1, 0] = current_prediction[0, 0]

            #error/warning line

        if run >= 2:  # Ignore the first two runs to mitigate potential outliers
            all_predictions.append(np.mean(hourly_predictions))

    if all_predictions:
        return np.mean(all_predictions)  # Average the predictions from all considered runs
    else:
        return None


base_directory_name = 'stock_data_2024-02-01_to_2024-03-08'
base_directory_path = os.path.join(os.getcwd(), base_directory_name)
output_file_path = os.path.join(base_directory_path, 'prediction_summary.csv')

# Ensure the output directory exists
os.makedirs(base_directory_path, exist_ok=True)

# Prepare the output file
with open(output_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Stock Ticker', 'Current Price', 'Predicted Price', 'Actual Average Price'])

    # Iterate over each day's folder within the base directory
    for date_folder in sorted(os.listdir(base_directory_path)):
        date_folder_path = os.path.join(base_directory_path, date_folder)
        
        # Check if it's a folder and not a file
        if os.path.isdir(date_folder_path):
            # Now iterate over each CSV file in the day's folder
            for filename in os.listdir(date_folder_path):
                if filename.endswith('.csv'):
                    csv_file_path = os.path.join(date_folder_path, filename)
                    df = pd.read_csv(csv_file_path)

                    # Extract ticker from the filename
                    stock_ticker = filename.split('_')[0]

                    # Get the actual average price for the date
                    date_str = date_folder
                    actual_avg_price = fetch_5min_prices(stock_ticker, date_str)

                    # Prepare data for LSTM
                    hourly_prices = df['Price'].to_numpy()
                    X, y, scaler = prepare_data_for_lstm(hourly_prices, time_steps)
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


                    # Define the LSTM model
                    model = Sequential([
                        LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
                        Dropout(0.2),
                        LSTM(50),
                        Dropout(0.2),
                        Dense(1)
                    ])
                    model.compile(optimizer='adam', loss='mean_squared_error')

                    # Perform prediction runs and get the average predicted price
                    predicted_price = perform_prediction_runs(X_train, y_train, scaler)


                    # Write the data to the CSV
                    writer.writerow([date_folder, stock_ticker, df['Price'].iloc[-1], predicted_price, actual_avg_price])
                    print(f"Processed {stock_ticker} for {date_folder}: Current Price: {df['Price'].iloc[-1]}, Predicted Price: {predicted_price}, Actual Average Price: {actual_avg_price}")

print(f"Predictions written to {output_file_path}")