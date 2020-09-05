from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from piratebay import piratebay_search
from kickass import kickass_search
from zooqle import zooqle_search


app = Flask(__name__)
api = Api(app)


class Movies(Resource):
    def get(self):
        query = "+".join([value for value in request.args.to_dict().values()])
        data = piratebay_search(query) + kickass_search(query) + zooqle_search(query)
        new_data = [item for item in data if int(item.get("seeds")) > 10]
        new_data.sort(key=lambda k: int(k['seeds']), reverse=True)
        return jsonify({"Total_Length": len(new_data), "Movies": new_data})  # Fetches first column that is Employee ID


api.add_resource(Movies, '/Movies')  # Route_1

if __name__ == '__main__':
    app.run(port='3000')