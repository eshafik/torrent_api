from bs4 import BeautifulSoup as bs
import requests


def kickass_search(query):
    url = "https://kickass.unblockit.top/search.php?q="+query
    source = requests.get(url).text
    soup = bs(source, 'lxml')
    rows = soup.find_all("tr", {"id": "torrent_latest_torrents12975568"})
    data = []
    for row in rows:
        single_data = {
            "title": row.find("a", class_="cellMainLink").get_text(),
            "size": row.find("td", class_="nobr center").get_text(),
            "seeds": row.find("td", class_="green center").get_text(),
            "peers": "",
            "resolution": "720p",
            "provider": "kickass",
            "magnet": row.find("a", title="Torrent magnet link")["href"],
        }
        data.append(single_data)
    return data


def check_magnet_link(tag):
    return True if tag.name == "a" and tag.attrs.get("title") == "Torrent magnet link" and len(
        tag.name["href"]) > 10 else False
