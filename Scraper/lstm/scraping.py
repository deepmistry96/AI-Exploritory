import os
import requests
import numpy as np
import pandas as pd
import csv
from datetime import datetime
from pytz import timezone
import pytz
# from sklearn.preprocessing import MinMaxScaler

# Polygon API for data fetching
POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"
symbol = input('Enter Stock Ticker Here: ')
market_open = 9.5
market_close = 16
eastern = timezone('US/Eastern')

# Function to fetch hourly prices
#def fetch_hourly_prices(date):
def fetch_hourly_prices(symbol, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/hour/{date}/{date}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data:
            df = pd.DataFrame(json_data['results'])
            df['datetime'] = pd.to_datetime(df['t'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(eastern)
            df = df.set_index('datetime').between_time(f'{int(market_open)}:30', f'{int(market_close)}:00')
            return df['c'].values, df.index  # Return prices and timestamps
        else:
            return np.array([]), []
    else:
        return np.array([]), []



# Fetch and write prices to a CSV file and store timestamps
start_date = datetime.now(eastern) - pd.DateOffset(days=6*30)
today_date_folder = datetime.now().strftime("%m_%d_%y")
datasets_path = os.path.join("new_datasets", today_date_folder)
os.makedirs(datasets_path, exist_ok=True)
hourly_prices = []
timestamps = []
start_date = datetime.now(eastern) - pd.DateOffset(days=6*30)

while start_date < datetime.now(eastern):
    if start_date.weekday() < 5:  # Skip weekends
        date_str = start_date.strftime('%Y-%m-%d')
        prices, times = fetch_hourly_prices(symbol, date_str)
        hourly_prices.extend(prices)
        timestamps.extend(times)
    start_date += pd.DateOffset(days=1)

# Find the last timestamp
last_timestamp = pd.to_datetime(timestamps[-1]) if timestamps else None

# Calculate the difference between the last timestamp and 4 PM
if last_timestamp:
    # 4 PM on the same day as the last timestamp in Eastern Time
    four_pm = last_timestamp.normalize().replace(hour=16, minute=0, second=0, microsecond=0)
    time_difference = (four_pm - last_timestamp).total_seconds() / 3600
    hours_until_close = int(time_difference)
else:
    hours_until_close = 'NA'

# Create the CSV file name
csv_file_name = os.path.join(datasets_path, f'{symbol}_{hours_until_close}_hours_till_close.csv')

# Write prices and timestamps to the CSV file
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Price'])
    for time, price in zip(timestamps, hourly_prices):
        writer.writerow([time, price])

print(f"Prices written to {csv_file_name}")
