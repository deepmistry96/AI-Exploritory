import os
import requests
import numpy as np
import pandas as pd
import csv
from datetime import datetime
from pytz import timezone
import pytz

POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"
symbol = input('Enter Stock Ticker Here: ')
eastern = timezone('US/Eastern')

def fetch_hourly_macd(date):
    url = f"https://api.polygon.io/v1/indicators/macd/{symbol}?range=1hour&date={date}&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data:
            df = pd.DataFrame(json_data['results'])
            return df['macd'].values, df.index
        else:
            return np.array([]), []
    else:
        return np.array([]), []

start_date = datetime.now(eastern) - pd.DateOffset(days=6*30)
macd_values = []
timestamps = []

while start_date < datetime.now(eastern):
    if start_date.weekday() < 5:
        date_str = start_date.strftime('%Y-%m-%d')
        macd, times = fetch_hourly_macd(date_str)
        macd_values.extend(macd)
        timestamps.extend(times)
    start_date += pd.DateOffset(days=1)

csv_file_name = f'{symbol}_macd_data.csv'

with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'MACD'])
    for time, macd in zip(timestamps, macd_values):
        writer.writerow([time, macd])

print(f"MACD data written to {csv_file_name}")
