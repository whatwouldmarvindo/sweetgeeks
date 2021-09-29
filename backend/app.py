from flask import Flask, request, jsonify
import response_builder
import json

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def main():
    city_name = request.args.get("cityName")
    statistics = response_builder.build_statistic(city_name)
    return jsonify(statistics)

@app.route('/test', methods=['GET'])
def test():
    city_name = request.args.get("cityName")
    statistics = [{'name' : "Grevenbroich", 'adresse' : "Breite Straße 1", 'modarea' : 'test', 'radabs' : 'test', 'kwh_kwp' : 'test', 'anzahl_0' : 'test', 'kw_17' : 'test', 'str_17' : "test"}]
    return json.dumps(statistics)







