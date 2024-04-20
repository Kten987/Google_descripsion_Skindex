from bs4 import BeautifulSoup
import requests
import re



def google_scrape(query):
    url = "https://www.google.com/search?q=" + query

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Save soup to a text file
    # with open("output.txt", "w", encoding="utf-8") as file:
    #     file.write(str(soup))
    results = []
    divs = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
    results = []
    for div in divs:
        if div.next_sibling and div.next_sibling.name != "div":
            print(str(div) + "\n" + "-"*5)
            
      
    # results = []
    # for div in divs[0:5]:
    #     if not div.find("span", class_="r0bn4c rQMQod"):
    #         text = div.get_text() + "\n" + "-"*5
    #         results.append(text)
    # for div in divs[0:5]:
    #     text = div.get_text() + "\n" + "-"*5
    #     results.append(text)
    return results

def main():
    query = "pyunkang+yul+cleansing+foam+description"
    results = google_scrape(query)
    # for result in results:
    #     print(result)

if __name__ == "__main__":
    main()