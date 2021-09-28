from flask import Flask, request, jsonify
import communicator

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def main():
    cityName = request.args.get("cityName")
    statistics = communicator.buildStatistic(cityName)
    return jsonify(statistics)







