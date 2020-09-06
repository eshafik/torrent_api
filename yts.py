from bs4 import BeautifulSoup
import requests

from title_checker import check_title


def yts_search(query):
    print("on yts..........")
    url = "https://yts.mx/ajax/search?query=" + query
    content = requests.get(url)
    data = content.json()
    if data.get("data"):
        results = []
        for item in data.get("data"):
            content = requests.get(item.get("url"))
            soup = BeautifulSoup(content.text, 'lxml')
            rows = soup.find_all("div", class_="modal-torrent")
            for row in rows:
                single_data = {
                    "title": item.get("title"),
                    "size": row.find_all("p", class_="quality-size")[1].get_text(),
                    "seeds": "100",
                    "peers": "",
                    "resolution": row.find("div", class_="modal-quality")["id"].split("-")[-1],
                    "provider": "piratebay",
                    "magnet": row.find_all("a")[1]["href"]
                }
                # check = check_title(query=query, data=single_data)
                # if check:
                #     data.append(single_data)
                results.append(single_data)
        return results
