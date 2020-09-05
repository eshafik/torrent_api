from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen


def get_soup(site):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'lxml')
        return soup
    except:
        print("site: ", site)


def search_1337x(query):
    url = f"https://1337x.to/search/{query}/1/"
    soup = get_soup(url)
    rows = soup.find_all("tr")
    data = []
    for row in rows[1:10]:
        size = row.find("td", ["coll-4", "size", "mob-user"]).get_text().split()
        url = "https://1337x.to" + row.find_all("a")[1]["href"]
        soup = get_soup(url)
        single_data = {
            "title": row.find_all("a")[1].get_text(),
            "size": size[0] + " " + size[1][:2],
            "seeds": row.find("td", class_="coll-2 seeds").get_text(),
            "peers": row.find("td", class_="coll-3 leeches").get_text(),
            "resolution": "720p",
            "provider": "1337x",
            "magnet": soup.find("a", href=re.compile('^magnet:?.+'))["href"]
        }
        data.append(single_data)

    return data
