import os
import requests
import pandas as pd
from datetime import datetime
from pytz import timezone, UTC
import csv
import time

# Configuration
tickers = ["TSLA", "AMD", "AMZN", "QQQ", "BABA", "TSM", "NVDA", "PDD", "AAPL", "KO", "SPY", "WMT", "ORCL", "CRM"]
POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"
eastern = timezone('US/Eastern')

# User date input
start_input = input("Enter start date (YYYY-MM-DD): ")
end_input = input("Enter end date (YYYY-MM-DD): ")

start_date = datetime.strptime(start_input, '%Y-%m-%d')
end_date = datetime.strptime(end_input, '%Y-%m-%d')

# Date range setup
date_range = pd.date_range(start_date, end_date)

# Create output directory
main_output_directory = f"stock_data_{start_input}_to_{end_input}"
os.makedirs(main_output_directory, exist_ok=True)

# Fetch prices with retries
def fetch_with_retries(url, max_retries=5, initial_wait=1.0):
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = requests.get(url, timeout=20)  # Increased timeout
            if response.status_code == 200:
                return response
            else:
                print(f"Error: Received status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}, retrying in {initial_wait} seconds...")
            time.sleep(initial_wait)
            initial_wait *= 2  # Double the wait time for the next retry
            retry_count += 1
    print("Max retries exceeded.")
    return None

def fetch_hourly_prices(symbol, cutoff_date):
    start_date = cutoff_date - pd.DateOffset(years=1)
    data = []
    for single_date in pd.date_range(start_date, cutoff_date):
        date_str = single_date.strftime('%Y-%m-%d')
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/hour/{date_str}/{date_str}?apiKey={POLYGON_API_KEY}&sort=asc"
        response = fetch_with_retries(url)
        if response and response.status_code == 200:
            json_data = response.json()
            if 'results' in json_data:
                for result in json_data['results']:
                    dt = pd.to_datetime(result['t'], unit='ms').tz_localize(UTC).tz_convert(eastern)
                    if '09:30' <= dt.strftime('%H:%M') <= '16:00':
                        data.append([dt.strftime('%Y-%m-%d %H:%M:%S'), result['c']])
    return data

# Main processing
for single_date in date_range:
    date_folder = os.path.join(main_output_directory, single_date.strftime('%Y-%m-%d'))
    os.makedirs(date_folder, exist_ok=True)
    
    for symbol in tickers:
        print(f"Processing {symbol} for {single_date.strftime('%Y-%m-%d')}")
        hourly_data = fetch_hourly_prices(symbol, single_date)
        
        csv_filename = os.path.join(date_folder, f"{symbol}_{single_date.strftime('%Y-%m-%d')}.csv")
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Timestamp', 'Price'])
            writer.writerows(hourly_data)
        
        print(f"Data for {symbol} on {single_date.strftime('%Y-%m-%d')} written to {csv_filename}")
