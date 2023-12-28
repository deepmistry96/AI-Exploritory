# import requests
# import pandas as pd

# import pdb
# pdb.set_trace()


# IEX_API_KEY = "pk_771e192b82674c9bb33fa6ae7259f22c"  # Replace with your IEX Cloud API key
# symbol = "AAPL"  # Replace with your desired ticker

# # IEX Cloud URL for historical data
# url = f"https://cloud.iexapis.com/stable/stock/{symbol}/intraday-prices?token={IEX_API_KEY}"

# response = requests.get(url)

# try: 
#     # Convert the response to a DataFrame
#     data = pd.DataFrame(response.json())

#     if data.empty:
#         print("No data fetched. Please check the ticker symbol or API availability.")
#     else:
#         # Process or analyze the data as needed
#         print(data.head())  # Print the first few rows of data
# except Exception as e:
#     print(f"An error occurred: {e}")

import requests
import pandas as pd
import datetime

# Set your API key and ticker symbol
IEX_API_KEY = "pk_771e192b82674c9bb33fa6ae7259f22c"  # Replace with your actual IEX Cloud API key
symbol = "AAPL"  # Replace with your desired ticker

# Function to fetch data for a single day
def fetch_data(date):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/intraday-prices?token={IEX_API_KEY}&exactDate={date}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        print(f"Error fetching data for {date}: {response.status_code}")
        return pd.DataFrame()

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Calculate the date range for the past year
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=1)

# Generate a list of dates in the range
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Loop over each date, fetch data, and append it to the DataFrame
for single_date in date_range:
    date_str = single_date.strftime("%Y%m%d")
    daily_data = fetch_data(date_str)
    all_data = pd.concat([all_data, daily_data], ignore_index=True)

# Export the data to a CSV file
all_data.to_csv("stock_data.csv", index=False)

print("Data retrieval complete. Check the 'stock_data.csv' file.")

