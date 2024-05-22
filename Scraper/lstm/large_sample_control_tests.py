import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import tensorflow as tf
import csv

#set seeds
np.random.seed(42)
tf.random.set_seed(42)
time_steps = 120

#prepare lstm data
def prepare_data_for_lstm(prices, time_steps=120):
    prices = np.array(prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])
    return np.array(X), np.array(y), scaler

#get user date
date_input = input("Enter the date (YYYY-MM-DD): ")
date_parts = date_input.split("-")
directory_path = f'./new_datasets/{date_parts[1]}_{date_parts[2]}_{date_parts[0][2:]}'

#output path
output_file_path = './prediction_summary.csv'

#ensure output dir
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

#prepare output file
with open(output_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Stock Ticker', 'Current Price', 'Predicted Price'])

    #iterate files
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(csv_file_path)

            #extract ticker
            stock_ticker = filename.split('_')[0]

            #last price
            current_price = df['Price'].iloc[-1]

            #prepare data
            hourly_prices = df['Price'].to_numpy()
            X, y, scaler = prepare_data_for_lstm(hourly_prices)
            X = X.reshape((X.shape[0], X.shape[1], 1))
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

            #lstm model
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
                Dropout(0.1),
                LSTM(50, return_sequences=False),
                Dropout(0.1),
                Dense(1)
            ])
            model.compile(optimizer='adam', loss='mean_squared_error')

            #train and predict
            predictions = {1: [], 2: [], 3: [], 4: [], 5: []}

            for run in range(8):  # Total runs
                model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
                
                #predict 1-5 hours
                ###change back to 5
                for hour_ahead in range(1, 6):
                    if hour_ahead == 1:
                        last_sequence = X[-1][-time_steps+1:].reshape((1, time_steps-1, 1))
                        last_sequence = np.insert(last_sequence, time_steps-1, X[-1][-1], axis=1)
                    else:
                        last_sequence = np.roll(last_sequence, -1, axis=1)
                        last_sequence[0, -1, 0] = predicted_price_scaled

                    predicted_price_scaled = model.predict(last_sequence)
                    predicted_price = scaler.inverse_transform(predicted_price_scaled.reshape(-1, 1))[0, 0]
                    predictions[hour_ahead].append(predicted_price)

            #average predictions
            all_predictions = sum(predictions.values(), [])
            if len(all_predictions) > 0:
                overall_average_prediction = np.mean(all_predictions)
                writer.writerow([stock_ticker, current_price, overall_average_prediction])
                print(f"Processed {stock_ticker}: Current Price: {current_price}, Overall Average Predicted Price: {overall_average_prediction}")
            else:
                print(f"Insufficient data for {stock_ticker}, skipped.")

print(f"Predictions written to {output_file_path}")
