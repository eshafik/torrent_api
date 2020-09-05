from bs4 import BeautifulSoup
import requests


def piratebay_search(query):
    print("search key: ", query)
    url = f"https://piratebay.party/search/{query}/1/99/0"
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'lxml')
    rows = soup.find_all("tr")
    data = []
    for row in rows[1:-1]:
        single_data = {
            "title": row.find_all("a")[1].get_text(),
            "size": row.find_all("td", align="right")[0].get_text(),
            "seeds": row.find_all("td", align="right")[1].get_text(),
            "peers": row.find_all("td", align="right")[2].get_text(),
            "resolution": "720p",
            "provider": "piratebay",
            "magnet": row.find_all("a")[2]["href"]
        }
        data.append(single_data)
    return data