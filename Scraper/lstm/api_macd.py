import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"
symbol = "AAPL"
output_file = "historical_hourly_prices.csv"
market_open = 9.5
market_close = 16

def fetch_hourly_prices(date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/hour/{date}/{date}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data:
            df = pd.DataFrame(json_data['results'])
            df['datetime'] = pd.to_datetime(df['t'], unit='ms')
            df = df.set_index('datetime').between_time(f'{int(market_open)}:30', f'{int(market_close)}:00')
            return df['c'].values  # Extract only closing prices
        else:
            return np.array([])
    else:
        return np.array([])

start_date = datetime.now() - timedelta(days=6*30)
hourly_prices = []

while start_date < datetime.now():
    if start_date.weekday() < 5:  # Skip weekends
        date_str = start_date.strftime('%Y-%m-%d')
        daily_prices = fetch_hourly_prices(date_str)
        hourly_prices.extend(daily_prices)
    start_date += timedelta(days=1)

# Convert the list to a NumPy array
hourly_prices_array = np.array(hourly_prices)

# Save to CSV
pd.DataFrame({'Hourly Prices': hourly_prices_array}).to_csv(output_file, index=False)
print(f"Data written to {output_file}")
