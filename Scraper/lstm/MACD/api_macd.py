import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz

def fetch_macd_for_hours(symbol, start_datetime, api_key, hours=10):
    print(f"Fetching MACD data for {symbol} from {start_datetime}")
    start_date_str = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    end_datetime = start_datetime + timedelta(hours=hours)
    end_date_str = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    url = f"https://api.polygon.io/v1/indicators/macd/{symbol}?range=1hour&from={start_date_str}&to={end_date_str}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data and 'values' in json_data['results']:
            data = []
            for entry in json_data['results']['values']:
                timestamp = datetime.fromtimestamp(entry['timestamp']/1000, tz=pytz.timezone('UTC'))
                macd = entry['value']
                data.append({'timestamp': timestamp, 'macd': macd})
            print(f"Data fetched successfully for period ending {end_date_str}")
            return pd.DataFrame(data)
        else:
            print(f"No data found for period ending {end_date_str}")
            return pd.DataFrame()
    else:
        print(f"Failed to fetch data for period ending {end_date_str}")
        return pd.DataFrame()

def fetch_macd_yearly(symbol, api_key):
    end_date = datetime.now(pytz.timezone('UTC'))
    start_date = end_date - timedelta(days=365)
    all_data = pd.DataFrame()

    while start_date < end_date:
        macd_data = fetch_macd_for_hours(symbol, start_date, api_key, hours=24)
        if not macd_data.empty:
            all_data = pd.concat([all_data, macd_data], ignore_index=True).drop_duplicates(subset=['timestamp'])
            start_date = start_date + timedelta(hours=24) 
        else:
            start_date += timedelta(hours=24) 

    return all_data

POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"
symbol = "AAPL"

print("Starting MACD data fetch...")
macd_data = fetch_macd_yearly(symbol, POLYGON_API_KEY)

csv_file_name = f'MACD_{symbol}_yearly.csv'
macd_data.to_csv(csv_file_name, index=False)
print(f"MACD data written to {csv_file_name}")
