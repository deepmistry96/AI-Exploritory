import os
import requests
import numpy as np
import pandas as pd
import csv
from datetime import datetime
from pytz import timezone
import pytz
# from sklearn.preprocessing import MinMaxScaler

import pdb
# pdb.set_trace()

tickers = [
    # "TSLA",
    "AMD", 
    "AMZN", 
    # "QQQ", 
    # "BABA",
    # "TSM", 
    "NVDA", 
    # "PDD", 
    # "AAPL",
    # "KO",
    # "SPY",
    # "TSLA",
    # "WMT",
    # "ORCL",
    # "CRM"
    ]

POLYGON_API_KEY = "UEj08qcyC_Wy7BrWupey9WGN3vQ83JXr"

#Parameters, set to false to set to default
pull_date = "2024-02-13" #todays_date, 2024-02-13
pull_data = False #True # False
eastern = timezone('US/Eastern')


market_open = f"{pull_date} 09:30:00"  #"default" #9.5
market_close = f"{pull_date} 16:00:00" #"default" #16

market_open_datetime = datetime.strptime(market_open, '%Y-%m-%d %H:%M:%S')
market_close_datetime = datetime.strptime(market_close, '%Y-%m-%d %H:%M:%S')

tickerdata_open = "default" 
tickerdata_close = "default"

tickerdata_fidelity = "high"

input_csv_structure = "default" # ex: [ ticker_low, strike_price, ticker_high ]

data_fidelity = {
    'high': "second", 
    'medium': "minute", 
    'low': "hour" 
}


   
def fetch_hourly_prices(symbol, date):
    # pdb.set_trace()
    #url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/hour/{date}/{date}?apiKey={POLYGON_API_KEY}"
    url =  f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/{data_fidelity[tickerdata_fidelity]}/{date}/{date}?adjusted=true&sort=asc&limit=5000&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data:
            df = pd.DataFrame(json_data['results'])
            # pdb.set_trace()
            # for row in df.iterrows():
            #     print (pd.to_datetime(row[1]["t"], unit='ms'))

            #df['datetime'] = pd.to_datetime(df['t'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(eastern)
            df['t'] = pd.to_datetime(df['t'], unit='ms')
            # df = df.set_index('datetime').between_time(f'{int(market_open)}:30', f'{int(market_close)}:00')
            #test = pd.date_range(market_open, market_close, freq='5s')
            #df = df.set_index('t').between_time(market_open_datetime, market_close_datetime)
            # return df['c'].values, df.index
            return df, df.index
        else:
            return np.array([]), []
    else:
        return np.array([]), []

start_date = datetime.now(eastern) - pd.DateOffset(days=6*30)
today_date_folder = datetime.now().strftime("%y-%m-%d")
datasets_path = os.path.join("new_datasets", pull_date)
os.makedirs(datasets_path, exist_ok=True)

for symbol in tickers:
    hourly_prices = []
    timestamps = []
    start_date = datetime.now(eastern) - pd.DateOffset(days=6*30)
    
    # while start_date < datetime.now(eastern):
    #     if start_date.weekday() < 5: #<here
    #         date_str = start_date.strftime('%Y-%m-%d')
            
    #         #
    #         # prices, times = fetch_hourly_prices(symbol, date_str)
    #         prices, times = fetch_hourly_prices(symbol, pull_date)
            
            
            
    #         hourly_prices.extend(prices)
    #         timestamps.extend(times)
    #     start_date += pd.DateOffset(days=1)
    
    # prices, times = fetch_hourly_prices(symbol, pull_date)
    prices_df, times = fetch_hourly_prices(symbol, pull_date)

    last_timestamp = pd.to_datetime(timestamps[-1]) if timestamps else None
    # if last_timestamp:
    #     four_pm = last_timestamp.normalize().replace(hour=16, minute=0, second=0, microsecond=0)
    #     time_difference = (four_pm - last_timestamp).total_seconds() / 3600
    #     hours_until_close = int(time_difference)
    # else:
    #     hours_until_close = 'NA'
    
    csv_file_name = os.path.join(datasets_path, f'{symbol}_full_data.csv')
    # pdb.set_trace()
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(['Timestamp', 'Price'])
        # for time, price in zip(timestamps, hourly_prices):
        #     writer.writerow([time, price])
        df_split = prices_df.to_string().replace(" ", ",")

        df_split = df_split.replace(",,,,,,,,",",")
        df_split = df_split.replace(",,,,,,,",",")
        df_split = df_split.replace(",,,,,,",",")
        df_split = df_split.replace(",,,,,",",")
        df_split = df_split.replace(",,,,",",")
        df_split = df_split.replace(",,,",",")
        df_split = df_split.replace(",,",",")
    
        

        # # df_split = df_split.split("\n")
        # for line in df_split:
        #     pdb.set_trace()
        #     file.write(line) 
        file.writelines(df_split)


           


    print(f"Prices written to {csv_file_name}")
