import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os

# Load data
file_path = 'AAPL_lstm_data.csv'
data = pd.read_csv(file_path)
data = data.apply(pd.to_numeric, errors='coerce')
data.dropna(inplace=True)

# Splitting data into X (inputs) and y (outputs)
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Convert data types to float32
X = X.astype(np.float32)
y = y.astype(np.float32)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Reshape data for LSTM
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))

# Compile and train the model
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=50, batch_size=32)

# Predicting on test data
predicted_stock_price = model.predict(X_test)

# Fetching hourly prices for scaling
hourly_prices = pd.read_csv('AAPL_hourly_prices.csv')['Current_Price'].tolist()


# Fit scaler on original data
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit_transform(np.array(hourly_prices).reshape(-1, 1))

# Predict next 5 minutes
last_sequence = np.expand_dims(X[-1], axis=0)
next_5_minutes = model.predict(last_sequence)

# Reshape prediction for inverse transform
next_5_minutes_reshaped = next_5_minutes.reshape(-1, 1)

# Inverse transform to get original scale
next_5_minutes_price = scaler.inverse_transform(next_5_minutes_reshaped)

print("Next 5 minutes prediction (price):", next_5_minutes_price)
