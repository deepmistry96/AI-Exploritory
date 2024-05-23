import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import LearningRateScheduler
import tensorflow as tf
import csv
import os

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Prepare data for LSTM
def prepare_data_for_lstm(prices, time_steps=120, future_steps=5):
    prices = np.array(prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(time_steps, len(scaled_prices) - future_steps):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i + future_steps, 0])  # target is the price 'future_steps' days ahead

    return np.array(X), np.array(y), scaler

# Function to adjust learning rate
def scheduler(epoch, lr):
    if epoch < 10:
        return lr
    else:
        return lr * tf.math.exp(-0.1)

# Define the parameter ranges
time_steps_options = [30, 60, 90, 120, 200]
test_size_options = [0.1, 0.2, 0.3]
dropout_options = [0.1, 0.2, 0.3, 0.5]
unit_options = [50, 100, 150, 200]
learning_rate_options = [0.001, 0.01, 0.1]

# Folder with CSV files
folder_path = './10-day_MA_dataset/'

# Open a file to write the results for all files
output_filename = 'lstm_predictions5_AAPL_5hrs.csv'
with open(output_filename, 'w', newline='') as file:
    writer = csv.writer(file)

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        try:
            csv_file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(csv_file_path)
            hourly_prices = df['10_day_MA'].to_numpy()

            for time_steps in time_steps_options:
                for test_size in test_size_options:
                    for dropout_rate in dropout_options:
                        for units in unit_options:
                            for learning_rate in learning_rate_options:
                                X, y, scaler = prepare_data_for_lstm(hourly_prices, time_steps=time_steps, future_steps=5)  # future_steps is 5
                                if X.size > 0 and y.size > 0:
                                    predicted_prices = []
                                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                                    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
                                    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

                                    model = Sequential([
                                        LSTM(units, return_sequences=True, input_shape=(X_train.shape[1], 1)),
                                        Dropout(dropout_rate),
                                        LSTM(units, return_sequences=False),
                                        Dropout(dropout_rate),
                                        Dense(1)
                                    ])
                                    optimizer = Adam(learning_rate=learning_rate)
                                    model.compile(optimizer=optimizer, loss='mean_squared_error')
                                    lr_scheduler = LearningRateScheduler(scheduler)
                                    model.fit(X_train, y_train, epochs=50, batch_size=32, callbacks=[lr_scheduler])

                                    # Predict the future price after 5 days
                                    last_sequence = np.expand_dims(X[-1], axis=0)
                                    next_price_scaled = model.predict(last_sequence)
                                    next_price = scaler.inverse_transform(next_price_scaled.reshape(-1, 1))[0][0]
                                    predicted_prices.append(next_price)

                                    # Output results as before
                                    average_price = np.mean(predicted_prices)
                                    std_dev = np.std(predicted_prices)
                                    header_info = [filename, time_steps, test_size, dropout_rate, units, learning_rate]
                                    prediction_info = ["10-day MA prediction after 5 days:", average_price]
                                    std_dev_info = ["Standard Deviation:", std_dev]

                                    writer.writerow(header_info)
                                    writer.writerow(prediction_info)
                                    writer.writerow(std_dev_info)
                                    writer.writerow([])  # Add a blank line for separation
                                    print(f"Processed {filename}: Average {average_price:.2f}, Std Dev {std_dev:.2f}")

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

print("All predictions have been written to", output_filename)


