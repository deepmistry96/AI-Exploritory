import requests
import wikipedia
import websocket
import json
import time
import select
import textwrap
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
import threading
import yfinance as yf
import os 
import finnhub
from datetime import datetime, timedelta, timezone
from dateutil.tz import gettz
from bs4 import BeautifulSoup
import numpy as np
from sklearn.preprocessing import MinMaxScaler


finnhub_client = finnhub.Client(api_key="cjmo8s9r01qmdd9q4000cjmo8s9r01qmdd9q400g")

API_KEY = "citmec1r01qu27mo126gcitmec1r01qu27mo1270"
NEWS_API_KEY = "1e412cd6dc5640b383fc18477ad45b34"
ALPHAVANTAGE_API_KEY = "2JW0VYC6INQB3DD7"
def generate_filename(ticker):
    # Generate a unique filename based on the current timestamp and the stock ticker
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{ticker}_result_{timestamp}.txt"
def get_company_name(ticker):
    url = f"https://finnhub.io/api/v1/search?q={ticker}&token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "result" in data:
        results = data["result"]
        if results:
            first_result = results[0]
            company_name = first_result["description"]
            return company_name
    return None
def scrape_wikipedia_page(ticker, filename):
    try:
        # Fetch the page content
        page = wikipedia.page(ticker)
        content = page.content
        # Open the write file
        with open(filename, "w") as f:
            # Write the Wikipedia page content to the file
            f.write(f"{page.title}:\n\n")
            f.write(f"{content}\n\n")
        print("Wikipedia scraper results saved to", filename)
    except wikipedia.exceptions.PageError:
        print("No Wikipedia page found for the given company.")
    except wikipedia.exceptions.DisambiguationError as e:
        print("Multiple Wikipedia pages found. Please provide more specific details or choose a different ticker.")
        print("Possible options:")
        for option in e.options:
            print(option)
def ordinal_suffix(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return suffix

def get_past_earnings(ticker, filename):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={ALPHAVANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "quarterlyEarnings" in data and data["quarterlyEarnings"]:
        earnings = data["quarterlyEarnings"]
        earnings_filename = f"{filename}_earnings.txt"
        with open(earnings_filename, "a") as f:
            f.write(f"\nPast earnings for {ticker}:\n")
            for earning in earnings:
                date_obj = datetime.strptime(earning["fiscalDateEnding"], "%Y-%m-%d")
                formatted_date = f"{date_obj.strftime('%B')} {date_obj.day}{ordinal_suffix(date_obj.day)} {date_obj.year}"
                reported_eps = earning["reportedEPS"]
                estimated_eps = earning["estimatedEPS"]
                surprise_percentage = earning["surprise"]
                f.write(f"Date: {formatted_date}, Reported EPS: {reported_eps}, Estimated EPS: {estimated_eps}, Surprise %: {surprise_percentage}\n")
                f.flush()  # Flush the data immediately to the file
        print(f"Past earnings data saved to {earnings_filename}")
    else:
        print(f"No earnings data found for {ticker}.")

def get_balance_sheet(ticker, filename):
    url = f"https://finnhub.io/api/v1/stock/financials-reported?symbol={ticker}&statement=balance_sheet&freq=annual&token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "financials" in data:
        balance_sheet_data = data["financials"]
        if balance_sheet_data:
            with open(filename, "a") as f:
                f.write("\nBalance Sheet:\n")
                for item in balance_sheet_data:
                    for key, value in item.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
            print(f"Balance sheet data saved to {filename}")
        else:
            print("No balance sheet data found.")
    else:
        print("Error occurred while retrieving balance sheet data.")
def get_income_statement(ticker, filename):
    url = f"https://finnhub.io/api/v1/stock/financials-reported?symbol={ticker}&statement=income_statement&freq=annual&token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "financials" in data:
        income_statement_data = data["financials"]
        if income_statement_data:
            with open(filename, "a") as f:
                f.write("\nIncome Statement:\n")
                for item in income_statement_data:
                    for key, value in item.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
            print(f"Income statement data saved to {filename}")
        else:
            print("No income statement data found.")
    else:
        print("Error occurred while retrieving income statement data.")








def get_cash_flow_statement(ticker, filename):
    url = f"https://finnhub.io/api/v1/stock/financials-reported?symbol={ticker}&statement=cash_flow_statement&freq=annual&token={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Function to recursively search and replace in nested dictionaries
    def search_and_replace_in_dict(d):
        for key, value in d.items():
            if key == "concept" and isinstance(value, str):
                d[key] = value.replace("us-gaap_", "")  # Remove the 'us-gaap_' prefix
            elif isinstance(value, dict):
                search_and_replace_in_dict(value)  # Recursive call for nested dictionary
            elif isinstance(value, list):
                for item in value:  # Recursive call for each dictionary in the list
                    if isinstance(item, dict):
                        search_and_replace_in_dict(item)

    # If the key 'data' exists in the response and it's not empty
    if data.get("data"):
        for report in data["data"]:
            if "report" in report:
                # Apply the search and replace function to each report
                search_and_replace_in_dict(report)

    # Write the modified data to the file
    with open(filename, "w") as f:
        f.write("Cash Flow Statement API Response:\n")
        # Convert the dictionaries into single-line strings and write them line by line
        for item in data.get("data", []):  # Iterate through each item in the 'data' list
            f.write(json.dumps(item) + '\n')  # Convert the dictionary to a single-line JSON string and write to the file

    print("Cash flow statement data saved to", filename)







def get_support_resistance_levels(ticker, timeframe='D'):
    try:
        # Fetch support and resistance levels using the Finnhub API
        response = finnhub_client.support_resistance(ticker, timeframe)
        levels = response.get("levels", [])

        if levels:
            # Print or save the levels as needed
            print("Support and Resistance Levels for", ticker)
            for i, level in enumerate(levels, start=1):
                print(f"Level {i}: {level}")
        else:
            print(f"No support and resistance levels found for {ticker}.")

    except Exception as e:
        print(f"Error occurred while fetching support and resistance levels: {e}")

def get_key_financial_ratios(ticker, filename):
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={ticker}&metric=all&token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data:
        ratios_data = data
        if ratios_data:
            with open(filename, "a") as f:
                f.write("\nKey Financial Ratios:\n")
                for key, value in ratios_data.items():
                    f.write(f"{key}: {value}\n")
            print("Key financial ratios data saved to", filename)
        else:
            print("No key financial ratios data found.")
    else:
        print("Error occurred while retrieving key financial ratios data.")
def get_technical_indicators(ticker, filename):
    url = f"https://finnhub.io/api/v1/indicator?symbol={ticker}&resolution=D&from=1572651390&to=1575243390&indicator=sma&timeperiod=3&token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "sma" in data:
        sma_data = data["sma"]
        if sma_data:
            with open(filename, "a") as f:
                f.write("\nTechnical Indicators:\n")
                for item in sma_data:
                    f.write(f"{item}\n")
            print("Technical indicators data saved to", filename)
        else:
            print("No technical indicators data found.")
    else:
        print("Error occurred while retrieving technical indicators data.")
def get_sector_performances(filename):
    url = f"https://finnhub.io/api/v1/stock/metric?metric=price&token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    with open(filename, "a") as f:
        f.write("Sector Performances API Response:\n")
        f.write(json.dumps(data, indent=2) + "\n")
    if "price" in data:
        price_data = data["price"]
        if price_data:
            with open(filename, "a") as f:
                f.write("\nSector Performances:\n")
                for sector, performance in price_data.items():
                    f.write(f"{sector}: {performance}\n")
            print("Sector performances data saved to", filename)
        else:
            print("No sector performances data found.")
    else:
        print("Error occurred while retrieving sector performances data.")
def get_stock_news(ticker, filename):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}&language=en"
    response = requests.get(url)
    data = response.json()
    if "articles" in data:
        articles = data["articles"]
        if articles:
            with open(filename, "a") as f:
                f.write("\nRecent News:\n")
                for article in articles:
                    title = article["title"]
                    description = article["description"]
                    # Remove any trailing ellipsis ("...")
                    if description.endswith("…"):
                        description = description[:-1]
                    # Wrap the description to avoid truncation
                    wrapped_description = textwrap.fill(description, width=80)
                    # You can also extract other relevant information like "publishedAt", "url", etc.
                    f.write(f"Title: {title}\nDescription: {wrapped_description}\n\n")
            print("News articles saved to", filename)
        else:
            print(f"No news articles found for {ticker}.")
    else:
        print("Error occurred while fetching news articles.")


def ordinal(number):
    """Return number with ordinal suffix."""
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme. 
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = suffixes.get(number % 10, 'th')
    return f"{number}{suffix}"

def get_hourly_prices(ticker, filename):
    now = int(time.time())
    one_year_ago = now - (2 * 365 * 24 * 3600)  # 1 year in seconds
    batch_size = 350  # Number of data points per batch

    num_batches = (now - one_year_ago) // (3600 * batch_size) + 1

    for batch in range(num_batches):
        start_timestamp = one_year_ago + (batch * 3600 * batch_size)
        end_timestamp = start_timestamp + (3600 * batch_size)

        url = f"https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=1&from={start_timestamp}&to={end_timestamp}&token={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "c" in data and "t" in data:
            close_prices = data["c"]
            timestamps = data["t"]

            with open(filename, "a") as f:
                for timestamp, close_price in zip(timestamps, close_prices):
                    # Convert to Eastern Time
                    date_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc).astimezone(gettz('America/New_York'))
                    
                    if date_time.hour >= 9 and (date_time.hour < 16 or (date_time.hour == 16 and date_time.minute == 0)):
                        formatted_date = f"{date_time.strftime('%B')} {ordinal(date_time.day)} {date_time.year}"
                        formatted_time = date_time.strftime('%I:%M %p')
                        formatted_data = f"The price for {ticker} on {formatted_date} at {formatted_time} ET was {close_price:.4f}"
                        f.write(formatted_data + "\n")
                    
            print(f"Batch {batch + 1}/{num_batches} of hourly price data saved to {filename}")
        else:
            print(f"No hourly price data found for batch {batch + 1}/{num_batches}.")


if __name__ == "__main__":
    ticker = input("Enter a stock ticker: ")
    filename = generate_filename(ticker)

    if os.path.exists(filename):
        os.remove(filename)  # Remove the existing file if it exists

    # Create a thread for data retrieval

def get_company_description(company_name):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={company_name}&utf8="
    response = requests.get(url)
    data = response.json()
    if "query" in data and "search" in data["query"]:
        search_results = data["query"]["search"]
        if search_results:
            top_result = search_results[0]
            page_title = top_result["title"]
            return fetch_wikipedia_page_intro(page_title)
    return None
def fetch_wikipedia_page_intro(page_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=true&explaintext=true&titles={page_title}"
    response = requests.get(url)
    data = response.json()
    if "query" in data and "pages" in data["query"]:
        pages = data["query"]["pages"]
        for page_id, page_data in pages.items():
            if "extract" in page_data:
                extract = page_data["extract"]
                return extract
    return None
def prepare_data_for_lstm(raw_data, time_steps=60):
    # Extract prices from the raw data
    prices = []
    for line in raw_data.split('\n'):
        if "The price for" in line:
            price = float(line.split('was ')[-1])
            prices.append(price)

    # Convert to a numpy array
    prices = np.array(prices).reshape(-1, 1)

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    # Create sequences
    X = []
    for i in range(len(scaled_prices) - time_steps):
        X.append(scaled_prices[i:i + time_steps])

    return np.array(X)
def get_companies_in_same_sector(ticker, filename):
    url = f"https://finnhub.io/api/v1/stock/peers?symbol={ticker}&token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data and isinstance(data, list):
        peers = data
        with open(filename, "a") as f:
            f.write("\nCompanies in the same sector:\n")
            for peer_ticker in peers:
                company_name = get_company_name(peer_ticker)
                if company_name:
                    company_description = get_company_description(company_name)
                    f.write(f"Company: {company_name}\n")
                    f.write(f"Description: {company_description}\n\n")
    else:
        print(f"No peers found for {ticker}.")
# Declare a global variable to store the last price received from the WebSocket
last_price = None
is_initial_retrieval_done = False
# ... (Your other data retrieval functions)
def on_message(ws, message):
    global last_price, is_initial_retrieval_done  # Reference the global variables
    data = json.loads(message)
    if "data" in data and "p" in data["data"][0]:
        price = data["data"][0]["p"]
        symbol = data["data"][0]["s"]
        # Only proceed if the price has changed
        if last_price is None or price != last_price:
            last_price = price
            # Perform initial data retrieval for the corresponding stock ticker
            if not is_initial_retrieval_done:
                filename = generate_filename(symbol)
                company_name = get_company_name(symbol)
                if company_name:
                    with open(filename, "a") as f:
                        f.write(f"{company_name}\n")
                    # Call data retrieval functions here (without print statements to avoid repetition)
                    get_past_earnings(symbol, filename)
                    scrape_wikipedia_page(company_name, filename)
                    get_balance_sheet(symbol, filename)
                    get_income_statement(symbol, filename)
                    get_cash_flow_statement(symbol, filename)
                    get_key_financial_ratios(symbol, filename)
                    get_technical_indicators(symbol, filename)
                    get_sector_performances(filename)
                    get_stock_news(symbol, filename)
                is_initial_retrieval_done = True
                # Stop the WebSocket connection after initial data retrieval
                ws.close()
def on_error(ws, error):
    print("WebSocket Error:", error)
def on_close(ws):
    print("### WebSocket closed ###")
def non_blocking_send(ws, data):
    ready_to_send = select.select([], [ws.sock], [], 5)  # 5 seconds timeout
    if ready_to_send[1]:  # If the WebSocket is ready to send
        ws.send(data)
        return True
    else:
        return False
def on_open(ws):
    # This function will be called when the WebSocket is opened
    ticker = input("Enter a stock ticker: ")
    if non_blocking_send(ws, f'{{"type":"subscribe","symbol":"{ticker}"}}'):
        print("WebSocket subscription successful.")
    else:
        print("WebSocket subscription failed. Proceeding with data retrieval.")
    # Create a thread for data retrieval
    retrieval_thread = threading.Thread(target=perform_data_retrieval, args=(ticker,))
    retrieval_thread.start()
def perform_data_retrieval(ticker):
    # Perform data retrieval even if the WebSocket subscription failed
    company_name = get_company_name(ticker)
    if company_name:
        filename = generate_filename(ticker)
        with open(filename, "a") as f:
            f.write(f"{company_name}\n")
        # Call data retrieval functions here (without print statements to avoid repetition)
        get_past_earnings(ticker, filename)
        scrape_wikipedia_page(company_name, filename)
        get_balance_sheet(ticker, filename)
        get_income_statement(ticker, filename)
        get_cash_flow_statement(ticker, filename)
        get_key_financial_ratios(ticker, filename)
        get_technical_indicators(ticker, filename)
        get_sector_performances(filename)
        get_stock_news(ticker, filename)  
        get_hourly_prices(ticker, filename)
        get_companies_in_same_sector(ticker, filename) 
        get_support_resistance_levels(ticker, filename)
if __name__ == "__main__":
    # Declare a global variable to store the last price received from the WebSocket
    last_price = None
    is_initial_retrieval_done = False
    # Create the WebSocket connection and start listening for price updates
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={API_KEY}",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()