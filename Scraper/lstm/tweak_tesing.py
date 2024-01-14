import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import tensorflow as tf
import csv

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Load your dataset
csv_file_name = './datasets/AMZN_2_hours_till_close.csv'
df = pd.read_csv(csv_file_name)

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

hourly_prices = df['Price'].to_numpy()

# Define the parameter ranges
time_steps_options = [30, 60, 90, 120]
test_size_options = [0.1, 0.2, 0.3]
dropout_options = [0.1, 0.2, 0.3, 0.5]

# Open a file to write the results
with open('lstm_predictions.csv', 'a', newline='') as file:
    writer = csv.writer(file)

    for time_steps in time_steps_options:
        for test_size in test_size_options:
            for dropout_rate in dropout_options:
                if hourly_prices.size > 0:
                    X, y, scaler = prepare_data_for_lstm(hourly_prices, time_steps=time_steps)
                    if X.size > 0 and y.size > 0:
                        predicted_prices = []

                        for run in range(1, 11):  # 10 individual runs
                            print(f"Run {run} starting")

                            # Split the data
                            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                            X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
                            X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

                            # Build the LSTM model
                            model = Sequential([
                                LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
                                Dropout(dropout_rate),
                                LSTM(50, return_sequences=False),
                                Dropout(dropout_rate),
                                Dense(1)
                            ])
                            model.compile(optimizer='adam', loss='mean_squared_error')

                            # Train the model
                            model.fit(X_train, y_train, epochs=50, batch_size=32)

                            # Predict the price
                            last_sequence = np.expand_dims(X[-1], axis=0)
                            next_price_scaled = model.predict(last_sequence)
                            next_price = scaler.inverse_transform(next_price_scaled.reshape(-1, 1))[0][0]
                            predicted_prices.append(next_price)

                            # Write results to CSV file after each run
                            writer.writerow([f"Run {run} prediction: {next_price:.2f}"])

                        average_price = np.mean(predicted_prices)
                        std_dev = np.std(predicted_prices)

                        # Write the specifications and aggregated results
                        writer.writerow([f"time steps = {time_steps} || test size = {test_size} || AMZN 2 hour || Dropout = {dropout_rate}"])
                        writer.writerow(["All predictions:"] + [str(price) for price in predicted_prices])
                        writer.writerow([f"Average Predicted Price: {average_price:.2f}"])
                        writer.writerow([f"Standard Deviation: {std_dev:.2f}"])
                        writer.writerow([])  # Add a blank line for separation

                else:
                    print("No hourly prices available")
