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

# Main program
ticker = input("Enter a stock ticker: ")
company_name = get_company_name(ticker)

if company_name:
    print(f"{company_name}")
    try:
        page = wikipedia.page(company_name)
        content = page.content

        # Open the write file
        with open("wikiresult.txt", "a") as f:
            # Write the page content to the file
            f.write(company_name + ":\n" + content + "\n\n")
            print("Results saved to wikiresult.txt")
    except wikipedia.exceptions.PageError:
        print("No Wikipedia page found for the given company.")
    except wikipedia.exceptions.DisambiguationError as e:
        print("Multiple Wikipedia pages found. Please provide more specific details or choose a different ticker.")
        print("Possible options:")
        for option in e.options:
            print(option)
else:
    print("No company name found for the given ticker.")
