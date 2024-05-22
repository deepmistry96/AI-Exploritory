import os
import requests
import numpy as np
import pandas as pd
import csv
from datetime import datetime
from pytz import timezone

#list of tickers
tickers = [
    "AMD", 
    "AMZN", 
    "QQQ", 
    "BABA",
    "TSM", 
    "NVDA", 
    "PDD", 
    "AAPL",
    "KO",
    "SPY",
    "TSLA",
    "WMT",
    "ORCL",
    "CRM",
]

POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"
market_open = 10
market_close = 16
central = timezone('US/Central')

#fetch 5min prices
def fetch_5min_prices(symbol, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/minute/{date}/{date}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data:
            df = pd.DataFrame(json_data['results'])
            df['datetime'] = pd.to_datetime(df['t'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(central)
            df = df.set_index('datetime').between_time(f'{int(market_open)}:00', f'{int(market_close)}:00')
            return df['c']
        else:
            return pd.Series([])
    else:
        return pd.Series([])

#input date
date_input = input("Enter the date (YYYY-MM-DD): ")
try:
    input_date = datetime.strptime(date_input, "%Y-%m-%d")
except ValueError:
    print("Invalid date format. Please enter date in YYYY-MM-DD format.")
    exit()

today_date = input_date.strftime("%Y-%m-%d")
avg_prices = {}

#calculate avg prices
for symbol in tickers:
    prices = fetch_5min_prices(symbol, today_date)
    if not prices.empty:
        avg_price = prices.mean()
        avg_prices[symbol] = avg_price

#write to csv
output_dir = "avg_prices"
os.makedirs(output_dir, exist_ok=True) #ensure dir exists
output_file = os.path.join(output_dir, f"average_prices_{today_date}.csv")

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Stock', 'Average Price'])
    for symbol, avg_price in avg_prices.items():
        writer.writerow([symbol, avg_price])

print(f"Average prices saved to {output_file}")
