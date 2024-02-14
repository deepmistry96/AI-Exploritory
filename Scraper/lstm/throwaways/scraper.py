import requests
import wikipedia


API_KEY = "2JW0VYC6INQB3DD7"

def get_company_name(ticker):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "bestMatches" in data:
        best_matches = data["bestMatches"]
        if best_matches:
            first_match = best_matches[0]
            company_name = first_match["2. name"]
            return company_name

    return None

def get_historical_prices(ticker):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    historical_prices = []
    if "Time Series (Daily)" in data:
        time_series = data["Time Series (Daily)"]
        for date, values in time_series.items():
            open_price = values.get("1. open")
            close_price = values.get("4. close")
            historical_prices.append({"date": date, "open": open_price, "close": close_price})

    
    return historical_prices


def scrape_wikipedia_page(page_title):
    try:
        # Fetch the page content
        page = wikipedia.page(page_title)
        content = page.content

        # Open the write file
        with open("wikiresult.txt", "a") as f:  # Change "w" to "a" here to append instead of overwrite
            # Write the Wikipedia page content to the file
            f.write(f"{page.title}:\n\n")
            f.write(f"{content}\n\n")

        print("Wikipedia scraper results saved to wikiresult.txt")
    except wikipedia.exceptions.PageError:
        print("No Wikipedia page found for the given company.")
    except wikipedia.exceptions.DisambiguationError as e:
        print("Multiple Wikipedia pages found. Please provide more specific details or choose a different ticker.")
        print("Possible options:")
        for option in e.options:
            print(option)


def get_past_earnings(stock_ticker):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={stock_ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "quarterlyEarnings" in data:
        quarterly_earnings = data["quarterlyEarnings"]
        if quarterly_earnings:
            with open("wikiresult.txt", "a") as f:
                f.write("\nPast earnings for {stock_ticker}:\n")
                for earnings in quarterly_earnings:
                    date = earnings["fiscalDateEnding"]
                    reported_eps = earnings["reportedEPS"]
                    estimated_eps = earnings["estimatedEPS"]
                    surprise_percentage = earnings["surprisePercentage"]
                    f.write(f"Date: {date}, Reported EPS: {reported_eps}, Estimated EPS: {estimated_eps}, Surprise %: {surprise_percentage}\n")
            print("Past earnings data saved to wikiresult.txt")
        else:
            print(f"No earnings data found for {stock_ticker}.")
    else:
        print("Error occurred while retrieving earnings data.")

def get_company_overview(ticker):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data:
        with open("wikiresult.txt", "a") as f:
            f.write("\nCompany Overview:\n")
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
        print("Company overview data saved to wikiresult.txt")
    else:
        print("No company overview data found.")

def get_balance_sheet(ticker):
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "annualReports" in data:
        annual_reports = data["annualReports"]
        if annual_reports:
            with open("wikiresult.txt", "a") as f:
                f.write("\nBalance Sheet:\n")
                for report in annual_reports:
                    for key, value in report.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
            print("Balance sheet data saved to wikiresult.txt")
        else:
            print("No balance sheet data found.")
    else:
        print("Error occurred while retrieving balance sheet data.")

def get_income_statement(ticker):
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "annualReports" in data:
        annual_reports = data["annualReports"]
        if annual_reports:
            with open("wikiresult.txt", "a") as f:
                f.write("\nIncome Statement:\n")
                for report in annual_reports:
                    for key, value in report.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
            print("Income statement data saved to wikiresult.txt")
        else:
            print("No income statement data found.")
    else:
        print("Error occurred while retrieving income statement data.")

def get_cash_flow_statement(ticker):
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "annualReports" in data:
        annual_reports = data["annualReports"]
        if annual_reports:
            with open("wikiresult.txt", "a") as f:
                f.write("\nCash Flow Statement:\n")
                for report in annual_reports:
                    for key, value in report.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
            print("Cash flow statement data saved to wikiresult.txt")
        else:
            print("No cash flow statement data found.")
    else:
        print("Error occurred while retrieving cash flow statement data.")

def get_key_financial_ratios(ticker):
    url = f"https://www.alphavantage.co/query?function=KEY_FINANCIAL_RATIOS&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "ratios" in data:
        ratios = data["ratios"]
        if ratios:
            with open("wikiresult.txt", "a") as f:
                f.write("\nKey Financial Ratios:\n")
                for key, value in ratios.items():
                    f.write(f"{key}: {value}\n")
            print("Key financial ratios data saved to wikiresult.txt")
        else:
            print("No key financial ratios data found.")
    else:
        print("Error occurred while retrieving key financial ratios data.")

def get_technical_indicators(ticker):
    url = f"https://www.alphavantage.co/query?function=TECHNICAL_INDICATORS&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data:
        with open("wikiresult.txt", "a") as f:
            f.write("\nTechnical Indicators:\n")
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
        print("Technical indicators data saved to wikiresult.txt")
    else:
        print("No technical indicators data found.")

def get_sector_performances():
    url = f"https://www.alphavantage.co/query?function=SECTOR&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Rank A: Real-Time Performance" in data:
        performances = data["Rank A: Real-Time Performance"]
        if performances:
            with open("wikiresult.txt", "a") as f:
                f.write("\nSector Performances:\n")
                for sector, performance in performances.items():
                    f.write(f"{sector}: {performance}\n")
            print("Sector performances data saved to wikiresult.txt")
        else:
            print("No sector performances data found.")
    else:
        print("Error occurred while retrieving sector performances data.")

# Main program
ticker = input("Enter a stock ticker: ")
company_name = get_company_name(ticker)

if company_name:
    print(f"{company_name}")
    with open("wikiresult.txt", "w") as f:
        f.write(f"Stock Ticker: {ticker}\n")
        f.write(f"Company Name: {company_name}\n\n")
    
    get_past_earnings(ticker)
    scrape_wikipedia_page(company_name)
    get_company_overview(ticker)
    get_balance_sheet(ticker)
    get_income_statement(ticker)
    get_cash_flow_statement(ticker)
    get_key_financial_ratios(ticker)
    get_technical_indicators(ticker)
    get_sector_performances()
    historical_prices = get_historical_prices(ticker)
    if historical_prices:
        f.write("\nHistorical Price Data:\n")
        for data_point in historical_prices:
            date = data_point["date"]
            open_price = data_point["open"]
            close_price = data_point["close"]
            f.write(f"Date: {date}, Open: {open_price}, Close: {close_price}\n")
        print("Historical price data saved to wikiresult.txt")
    else:
        print("No historical price data found.")
else:
    print("No company name found for the given ticker.")