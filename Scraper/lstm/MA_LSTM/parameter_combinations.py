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
import keras_tuner as kt

np.random.seed(42)
tf.random.set_seed(42)

def prepare_data_for_lstm(prices, time_steps, future_steps=5):
    prices = np.array(prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)
    X, y = [], []
    for i in range(time_steps, len(scaled_prices) - future_steps):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i + future_steps, 0]) 
    return np.array(X), np.array(y), scaler

def scheduler(epoch, lr):
    if epoch < 10:
        return lr
    else:
        return lr * tf.math.exp(-0.1)

def build_model(hp):
    model = Sequential([
        LSTM(hp.Int('units', min_value=50, max_value=200, step=50), return_sequences=True, input_shape=(120, 1)),
        Dropout(hp.Float('dropout', min_value=0.1, max_value=0.5, step=0.1)),
        LSTM(hp.Int('units', min_value=50, max_value=200, step=50), return_sequences=False),
        Dropout(hp.Float('dropout', min_value=0.1, max_value=0.5, step=0.1)),
        Dense(1)
    ])
    model.compile(optimizer=Adam(hp.Choice('learning_rate', values=[0.001, 0.01, 0.1])),
                  loss='mean_squared_error')
    return model

folder_path = './10-day_MA_dataset/'
output_filename = 'lstm_predictions5_AAPL_10day.csv'
with open(output_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    for filename in os.listdir(folder_path):
        csv_file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(csv_file_path)
        hourly_prices = df['10_day_MA'].to_numpy()

        X, y, scaler = prepare_data_for_lstm(hourly_prices, time_steps=120)  # Fixed time_steps for tuning
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        tuner = kt.Hyperband(build_model,
                             objective='val_loss',
                             max_epochs=50,
                             factor=3,
                             directory='my_dir',
                             project_name=f'tuning_{filename}')

        lr_scheduler = LearningRateScheduler(scheduler)
        tuner.search(X_train, y_train, epochs=50, validation_split=0.2, callbacks=[lr_scheduler])

        best_model = tuner.get_best_models(num_models=1)[0]
        best_hyperparameters = tuner.get_best_hyperparameters(num_trials=1)[0]

        print(f"Best hyperparameters for {filename}: {best_hyperparameters.values}")

        last_sequence = np.expand_dims(X[-1], axis=0)
        next_price_scaled = best_model.predict(last_sequence)
        next_price = scaler.inverse_transform(next_price_scaled.reshape(-1, 1))[0][0]

        header_info = [filename] + list(best_hyperparameters.values.values())
        prediction_info = ["10-day MA prediction after 5 days:", next_price]
        writer.writerow(header_info)
        writer.writerow(prediction_info)
        writer.writerow([])

print("All predictions and parameters have been written to", output_filename)
