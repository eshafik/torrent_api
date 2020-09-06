from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from piratebay import piratebay_search
from kickass import kickass_search
from zooqle import zooqle_search
from yts import yts_search
from x1337 import search_1337x
from eztvtorrent import eztvtorrent_search

app = Flask(__name__)
api = Api(app)


class Movies(Resource):
    def get(self):
        query = ""
        for key, value in request.args.to_dict().items():
            if key.lower() == "search" or key.lower() == "year" or key.lower() == 'language':
                query = f"{query}+{value}"
            else:
                query = f"{query}+{key}+{value}"
        query = "+".join([value for value in request.args.to_dict().values()])
        query = "+".join(query.split())
        match = query.split("+")
        data = (piratebay_search(query) or []) + (kickass_search(query) or []) + (zooqle_search(query) or []) + (
                yts_search(query) or []) + (search_1337x(query) or [])
        print("data: ", len(data))
        new_data = [item for item in data if (item.get("seeds") and int(item.get("seeds")) > 10)]
        print("seeds filtering: ", len(new_data))
        new_data = (len(match) >= 2) and [item for item in new_data if (
                    match[0].lower() in item.get("title").lower() and match[1].lower() in item.get("title").lower())]
        print("final filter: ", len(new_data))
        new_data.sort(key=lambda k: int(k['seeds']), reverse=True)
        return jsonify({"Total_Length": len(new_data), "Movies": new_data})  # Fetches first column that is Employee ID


api.add_resource(Movies, '/Movies')  # Route_1

if __name__ == '__main__':
    app.run(port='3000')
