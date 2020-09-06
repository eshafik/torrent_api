from bs4 import BeautifulSoup
import requests

from title_checker import check_title


def eztvtorrent_search(query):
    url = "https://eztvtorrent.co/search?s=" + query
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    rows = soup.find_all("div", class_="box-item")
    data = []
    for row in rows:
        url = row.find("a")["href"]
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        items = soup.find("tbody").find_all("tr")
        for item in items:
            single_data = {
                "title": row.find("a")["title"],
                "size": item.find_all("td")[0].get_text(),
                "seeds": "100",
                "peers": "",
                "resolution": item.find_all("td")[1].get_text(),
                "provider": "eztv",
                "magnet": item.find_all("td")[3].find("a")["href"]
            }
            # check = check_title(query=query, data=single_data)
            # if check:
            #     data.append(single_data)

            data.append(single_data)
    return data
