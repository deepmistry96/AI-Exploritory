import requests

API_KEY = "2JW0VYC6INQB3DD7"

def get_past_earnings(stock_ticker):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={stock_ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "quarterlyEarnings" in data:
        quarterly_earnings = data["quarterlyEarnings"]
        if quarterly_earnings:
            print(f"Past earnings for {stock_ticker}:")
            for earnings in quarterly_earnings:
                date = earnings["fiscalDateEnding"]
                reported_eps = earnings["reportedEPS"]
                estimated_eps = earnings["estimatedEPS"]
                surprise_percentage = earnings["surprisePercentage"]
                print(f"Date: {date}, Reported EPS: {reported_eps}, Estimated EPS: {estimated_eps}, Surprise %: {surprise_percentage}")
        else:
            print(f"No earnings data found for {stock_ticker}.")
    else:
        print("Error occurred while retrieving earnings data.")

# Main program
stock_ticker = input("Enter a stock ticker: ")
get_past_earnings(stock_ticker)
