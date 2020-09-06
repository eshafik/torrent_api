from bs4 import BeautifulSoup
import requests


def td_search(query):
    url = "https://eztv.io/search/" + query
    soup = BeautifulSoup(requests.get(url).text, 'lxml')

    rows = soup.find_all("tr", class_="forum_header_border")
    if len(rows) > 6:
        rows = rows[:5]
    else:
        rows = rows

    data = []

    for row in rows[:5]:
        # print("seeds", row.find("td", class_="forum_thread_post_end").get_text())
        single_data = {
            "title": row.find("a", class_="epinfo").get_text(),
            "size": row.find_all("td", class_="forum_thread_post")[3].get_text(),
            "seeds": "11",
            "peers": "",
            "resolution": "720p",
            "provider": "torrentDownload",
            "magnet": row.find_all("a")[2]["href"]
        }
        data.append(single_data)
    return data
