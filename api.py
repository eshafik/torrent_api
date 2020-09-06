from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import concurrent.futures

from piratebay import piratebay_search
from kickass import kickass_search
from zooqle import zooqle_search
from yts import yts_search
from x1337 import search_1337x
from eztvtorrent import eztvtorrent_search

app = Flask(__name__)
api = Api(app)


def get_data(query):
    print("query with:", query)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        pirate = executor.submit(piratebay_search, query)
        kickass = executor.submit(kickass_search, query)
        x1337 = executor.submit(search_1337x, query)
        zooqle = executor.submit(zooqle_search, query)
        yts = executor.submit(yts_search, query)

        pirate_value = pirate.result()
        kickass_value = kickass.result()
        x1337_value = x1337.result()
        zooqle_value = zooqle.result()
        yts_value = yts.result()


        match = query.split("+")

        data = (pirate_value or []) + (kickass_value or []) + (x1337_value or []) + (
                yts_value or []) + (zooqle_value or [])
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
                lan_data = executor.submit(get_data, query)
                without_lan_data = executor.submit(get_data, query.replace(f"+{language}", ""))

                lan_data_value = lan_data.result()
                without_lan_data_value = without_lan_data.result()

                new_data = lan_data_value + without_lan_data_value
        else:
            new_data = get_data(query)

        # if (not new_data) and language:
        #     new_data = get_data(query.replace(f"+{language}", ""))
        #     new_data.sort(key=lambda k: int(k['seeds']), reverse=True)
        #     return jsonify(
        #         {"Total_Length": len(new_data), "Movies": new_data})  # Fetches first column that is Employee ID

        new_data.sort(key=lambda k: int(k['seeds']), reverse=True)
        return jsonify({"Total_Length": len(new_data), "Movies": new_data})  # Fetches first column that is Employee ID


api.add_resource(Movies, '/Movies')  # Route_1

if __name__ == '__main__':
    app.run(port='3000')
