from flask import Flask, request, jsonify
import response_builder

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def main():
    cityName = request.args.get("cityName")
    statistics = response_builder.buildStatistic(cityName)
    return jsonify(statistics)







