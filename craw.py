from bs4 import BeautifulSoup
import requests
import re

def google_scrape(query):
    url = "https://www.google.com/search?q=" + query

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    divs = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
    for div in divs[0:5]:
        text = div.get_text()
        results.append(text)
    return results

def main():
    query = "pyunkang yul cleansing foam description"
    results = google_scrape(query)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()