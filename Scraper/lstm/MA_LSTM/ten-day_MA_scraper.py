import os
import requests
import pandas as pd
from datetime import datetime, timedelta

POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"
BASE_URL = "https://api.polygon.io/v2/aggs/ticker/"

def fetch_stock_data(symbol, start_date, end_date):
    url = f"{BASE_URL}{symbol}/range/1/day/{start_date}/{end_date}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['results']
        return pd.DataFrame(data)
    else:
        print(f"Failed to fetch data for {symbol}")
        return pd.DataFrame()

def calculate_moving_average(df):
    df['t'] = pd.to_datetime(df['t'], unit='ms')
    df.set_index('t', inplace=True)
    df['10_day_MA'] = df['c'].rolling(window=10).mean()
    
    clean_df = df.dropna(subset=['10_day_MA'])
    
    return clean_df[['10_day_MA']]

specific_date = input("Enter the specific date (YYYY-MM-DD): ")
specific_date = datetime.strptime(specific_date, '%Y-%m-%d')

start_date = (specific_date - timedelta(days=365)).strftime('%Y-%m-%d')
end_date = specific_date.strftime('%Y-%m-%d')

ticker = input("Enter the stock ticker: ")

stock_data = fetch_stock_data(ticker, start_date, end_date)
ma_data = calculate_moving_average(stock_data)

output_file = f"10-day_MA_dataset/{ticker}_10_day_MA_{specific_date.strftime('%Y%m%d')}.csv"
ma_data.to_csv(output_file)
print(f"Data saved to {output_file}")
