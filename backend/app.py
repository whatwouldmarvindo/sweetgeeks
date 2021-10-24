from flask import Flask, request, jsonify
import response_builder
import json
from flask_mysqldb import MySQL

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


app.config['MYSQL_USER']        = 'root'
app.config['MYSQL_PASSWORD']    = 'toor'
app.config['MYSQL_HOST']        = '0.0.0.0'
app.config['MYSQL_DB']          = 'solarrechnerDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

db = MySQL(app)
@app.route('/')
def index():
        return "TEST"

@app.route('/databaseTest')
def databaseTest():
        cur = db.connection.cursor()
        cur.execute('''select * from staedte;''')
        results = cur.fetchall()
        print(results)
        return jsonify(results)

@app.route('/getBuildings')
def getBuildings(city_name):
        cur = db.connection.cursor()
        
        cur.execute('''select * from gebaeude where StadtID = (Select StadtID from Staedte where Name= \'''' + city_name +  '''\');''')
        results = cur.fetchall()
        #print(results)
        return jsonify(results)
@app.route('/getCityDetails')
def getCityDetails(city_name):
        cur = db.connection.cursor()
        city_name = request.args.get("cityName")
        cur.execute('''select * from Staedte where StadtID = (Select StadtID from Staedte where Name= \'''' + city_name +  '''\');''')
        results = cur.fetchall()
        #print(results)
        return jsonify(results)

@app.route('/GetCityData')
def getCityData():
    city_name = request.args.get("cityName")
    cur = db.connection.cursor()
    cur.execute('''select * from Staedte where StadtID = (Select StadtID from Staedte where Name= \'''' + city_name +  '''\');''')
    results1 = cur.fetchall()
    cur = db.connection.cursor()
    cur.execute('''select * from Gebaeude where StadtID = (Select StadtID from Staedte where Name= \'''' + city_name +  '''\');''')
    results2 = cur.fetchall()
    out = results1+results2

    return jsonify(out)
