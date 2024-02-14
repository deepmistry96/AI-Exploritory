import requests
import wikipedia
import websocket
import json
import time
import select
import textwrap
from datetime import datetime, timedelta, timezone
from dateutil.tz import gettz
from bs4 import BeautifulSoup
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import finnhub
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import threading
import os

def get_hourly_prices(ticker):
    now = int(time.time())
    one_year_ago = now - (365 * 24 * 3600)  # 1 year in seconds
    batch_size = 350  # Number of data points per batch

    num_batches = (now - one_year_ago) // (3600 * batch_size) + 1
    price_data = ""

    for batch in range(num_batches):
        start_timestamp = one_year_ago + (batch * 3600 * batch_size)
        end_timestamp = start_timestamp + (3600 * batch_size)

        url = f"https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=1&from={start_timestamp}&to={end_timestamp}&token={API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Debugging: Print API response
        print(f"API Response for batch {batch + 1}: {data}")

        if "c" in data and "t" in data:
            close_prices = data["c"]
            timestamps = data["t"]

            for timestamp, close_price in zip(timestamps, close_prices):
                # Convert to Eastern Time
                date_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc).astimezone(gettz('America/New_York'))
                formatted_date = f"{date_time.strftime('%B')} {ordinal(date_time.day)} {date_time.year}"
                formatted_time = date_time.strftime('%I:%M %p')
                formatted_data = f"The price for {ticker} on {formatted_date} at {formatted_time} ET was {close_price:.4f}"
                price_data += formatted_data + "\n"
        else:
            print(f"No hourly price data found for batch {batch + 1}/{num_batches}.")

    return price_data

get_hourly_prices()