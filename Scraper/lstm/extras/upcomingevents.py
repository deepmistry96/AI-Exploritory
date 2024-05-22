import requests
import urllib.parse
from bs4 import BeautifulSoup

def get_article_content(article_url):
    base_url = "https://finance.yahoo.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    article_url = urllib.parse.urljoin(base_url, article_url)

    response = requests.get(article_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        article_text = ""
        article_paragraphs = soup.find_all("p")
        for paragraph in article_paragraphs:
            article_text += paragraph.get_text() + "\n"
        return article_text
    else:
        print(f"Failed to fetch the article: {article_url}")
        return ""

def scrape_yahoo_finance_articles(stock_ticker):
    base_url = f"https://finance.yahoo.com/quote/{stock_ticker}/news?p={stock_ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        # Extract articles from the initial page
        article_elements = soup.find_all("h3", {"class": "Mb(5px)"})
        for article_element in article_elements:
            title = article_element.get_text()
            article_url = article_element.find("a")["href"]

            # Check if the article URL is valid
            if not article_url.startswith("http"):
                article_url = urllib.parse.urljoin(base_url, article_url)

            # Get the content of the article
            article_content = get_article_content(article_url)

            # Append the article information to the list
            articles.append({
                "title": title,
                "url": article_url,
                "content": article_content
            })

        # Extract more articles using AJAX requests
        offset = 0
        while True:
            json_url = f"https://finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm={stock_ticker};offset={offset}"
            json_response = requests.get(json_url, headers=headers).json()
            json_data = json_response.get("data", {}).get("items", [])
            if not json_data:
                break

            for data in json_data:
                title = data["headline"]
                article_url = data["link"]

                # Check if the article URL is valid
                if not article_url.startswith("http"):
                    article_url = urllib.parse.urljoin(base_url, article_url)

                # Get the content of the article
                article_content = get_article_content(article_url)

                # Append the article information to the list
                articles.append({
                    "title": title,
                    "url": article_url,
                    "content": article_content
                })

            offset += 10

        return articles
    else:
        print(f"Failed to fetch the webpage.")
        return []

if __name__ == "__main__":
    stock_ticker = input("Enter the stock ticker: ")
    articles = scrape_yahoo_finance_articles(stock_ticker)

    if articles:
        for idx, article in enumerate(articles, start=1):
            print(f"Title: {article['title']}")
            print(f"URL: {article['url']}")
            print(f"Content:\n{article['content']}\n")
            # Save the article content to a text file
            with open(f"article_{idx}.txt", "w", encoding="utf-8") as file:
                file.write(f"Title: {article['title']}\n")
                file.write(f"URL: {article['url']}\n")
                file.write(f"Content:\n{article['content']}\n")
    else:
        print(f"No upcoming events found for {stock_ticker}.")
