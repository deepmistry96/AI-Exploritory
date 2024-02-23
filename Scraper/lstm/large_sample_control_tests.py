import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import tensorflow as tf
import csv

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Prepare data for LSTM
def prepare_data_for_lstm(prices, time_steps=120):
    prices = np.array(prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])
    return np.array(X), np.array(y), scaler

# Directory containing the datasets
directory_path = './new_datasets/02_23_24'

# Output file path
output_file_path = './prediction_summary.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Prepare the output file
with open(output_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Stock Ticker', 'Current Price', 'Predicted Price'])

    # Iterate over each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(csv_file_path)

            # Extract stock ticker from filename
            stock_ticker = filename.split('_')[0]

            # Get the last price from the CSV file
            current_price = df['Price'].iloc[-1]

            # Prepare data for LSTM model
            hourly_prices = df['Price'].to_numpy()
            X, y, scaler = prepare_data_for_lstm(hourly_prices)
            X = X.reshape((X.shape[0], X.shape[1], 1))
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

            # Define LSTM model
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
                Dropout(0.1),
                LSTM(50, return_sequences=False),
                Dropout(0.1),
                Dense(1)
            ])
            model.compile(optimizer='adam', loss='mean_squared_error')

            # Train and predict with the model
            predictions = []
            for run in range(12):  # Total runs as per your setup
                model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
                last_sequence = X[-1].reshape((1, X.shape[1], 1))
                predicted_price_scaled = model.predict(last_sequence)
                predicted_price = scaler.inverse_transform(predicted_price_scaled.reshape(-1, 1))[0, 0]
                predictions.append(predicted_price)

            # Calculate average prediction from the last 10 runs
            if len(predictions) > 2:
                average_prediction = np.mean(predictions[2:])
                writer.writerow([stock_ticker, current_price, average_prediction])
                print(f"Processed {stock_ticker}: Current Price: {current_price}, Predicted Price: {average_prediction}")
            else:
                print(f"Insufficient data for {stock_ticker}, skipped.")

print(f"Predictions written to {output_file_path}")
