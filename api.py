from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import concurrent.futures

from piratebay import piratebay_search
from kickass import kickass_search
from torrent_download import td_search
from zooqle import zooqle_search
from yts import yts_search
from x1337 import search_1337x
from eztvtorrent import eztvtorrent_search

app = Flask(__name__)
api = Api(app)


def get_query_for_torrentdwn(query_params):

    query_param = {k.lower(): v for k, v in query_params.items()}
    if "search" and "season" and "episode" in query_param.keys():
        query = f"{query_param['search']}-s{query_param['season']}e{query_param['episode']}"
    elif "search" and "season" in query_param.keys():
        query = f"{query_param['search']}-s{query_param['season']}"
    else:
        query = f"{query_param['search']}"
    query = "-".join(query.split())
    print("t query:", query)
    return query


def get_data(query_dict):
    query = query_dict.get("query")
    t_query = query_dict.get("t_query")
    print("query with:", query)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        pirate = executor.submit(piratebay_search, query)
        kickass = executor.submit(kickass_search, query)
        x1337 = executor.submit(search_1337x, query)
        zooqle = executor.submit(zooqle_search, query)
        yts = executor.submit(yts_search, query)
        t_d = executor.submit(td_search, t_query)

        pirate_value = pirate.result()
        kickass_value = kickass.result()
        x1337_value = x1337.result()
        zooqle_value = zooqle.result()
        yts_value = yts.result()
        t_d_value = t_d.result()

        match = query.split("+")

        data = (pirate_value or []) + (kickass_value or []) + (x1337_value or []) + (
                yts_value or []) + (zooqle_value or []) + (t_d_value or [])
        print("data: ", len(data))
        new_data = [item for item in data if (item.get("seeds") and int(item.get("seeds")) > 10)]
        print("seeds filtering: ", len(new_data))
        new_data = (len(match) >= 2) and [item for item in new_data if (
                match[0].lower() in item.get("title").lower() and match[1].lower() in item.get("title").lower())]
        return new_data


class Movies(Resource):
    def get(self):
        query = ""
        language = None

        t_query = get_query_for_torrentdwn(request.args.to_dict())

        for key, value in request.args.to_dict().items():
            if key.lower() == "search" or key.lower() == "year" or key.lower() == 'language':
                query = f"{query}+{value}"
                language = (key.lower()=='language') and value
            else:
                query = f"{query}+{key}+{value}"
        query = "+".join([value for value in request.args.to_dict().values()])
        query = "+".join(query.split())

        if language:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                query_dict = {"query": query, "t_query": t_query}
                lan_data = executor.submit(get_data, query_dict)
                query_dict = {"query": query.replace(f"+{language}", ""), "t_query": t_query}
                without_lan_data = executor.submit(get_data, query_dict)

                lan_data_value = lan_data.result()
                without_lan_data_value = without_lan_data.result()

                lan_data_value.sort(key=lambda k: int(k['seeds']), reverse=True)
                without_lan_data_value.sort(key=lambda k: int(k['seeds']), reverse=True)

                new_data = lan_data_value + without_lan_data_value
        else:
            query_dict = {"query": query, "t_query": t_query}
            new_data = get_data(query_dict)
            new_data and new_data.sort(key=lambda k: int(k['seeds']), reverse=True)

        return jsonify({"Total_Length": len(new_data), "Movies": new_data})  # Fetches first column that is Employee ID


api.add_resource(Movies, '/Movies')  # Route_1

if __name__ == '__main__':
    app.run(port='3000')
