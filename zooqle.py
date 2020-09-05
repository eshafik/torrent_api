from bs4 import BeautifulSoup as bs
import requests


def zooqle_search(query):
    url = "https://zooqle.unblockit.top/search?q=" + query
    source = requests.get(url).text
    soup = bs(source, 'lxml')

    titles = soup.find_all('a', class_=' small', href=True)
    magnets = soup.find_all('a', title='Magnet link', href=True)
    sizes = soup.find_all("div", class_="progress-bar prog-blue prog-l")
    seeders = soup.find_all("div", class_="progress-bar smaller prog-green prog-l")
    peers = soup.find_all("div", class_="progress-bar smaller prog-yellow prog-r")

    t_len = len(titles)
    m_len = len(magnets)
    si_len = len(sizes)
    se_len = len(seeders)
    p_len = len(peers)

    l = min(t_len, m_len, si_len, se_len, p_len)
    data = []
    for title, size, seeds, peers, magnet in zip(titles[t_len - l:], sizes[si_len - l:], seeders[se_len - l:], peers,
                                                 magnets[m_len - l:]):
        single_data = {
            "title": title['href'][1:-11],
            "size": size.get_text(),
            "seeds": seeds.get_text(),
            "peers": peers.get_text(),
            "resolution": "720p",
            "provider": "zooqle",
            "magnet": magnet["href"]
        }
        data.append(single_data)
    return data
