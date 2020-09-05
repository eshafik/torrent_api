from bs4 import BeautifulSoup
import requests


def yts_search(query):
    url = "https://yts.mx/ajax/search?query=" + query
    content = requests.get(url)
    data = content.json()
    if data:
        results = []
        for item in data.get("data"):
            content = requests.get(item.get("url"))
            soup = BeautifulSoup(content.text, 'lxml')
            rows = soup.find_all("div", class_="modal-torrent")
            for row in rows:
                single_data = {
                    "title": item.get("title"),
                    "size": row.find_all("p", class_="quality-size")[1].get_text(),
                    "seeds": "",
                    "peers": "",
                    "resolution": row.find("div", class_="modal-quality")["id"].split("-")[-1],
                    "provider": "piratebay",
                    "magnet": row.find_all("a")[1]["href"]
                }
                results.append(single_data)
        return results