import json
import requests
import os
import pathlib
import time

def list_files(path):
    current_path = pathlib.Path(path)
    files = os.listdir(current_path)

    for file in files.copy():
        if not file.endswith(".json"):
            files.remove(file)

    print(files)
    return files
def getData(city):
    s_city = "\"" + city.replace("_"," ").replace("ue","ü").replace("oe","ö").replace("ue","ü").replace("##","/").replace("ss","ß") + "\""
    URL = "https://overpass-api.de/api/interpreter?data="
    QUERY = """
    [out:json];
    area[name=""" + s_city + """]->.searchArea;
    (
      way["building"="public"](area.searchArea);
      way["building"="dormitory"](area.searchArea);
      way["building"="civic"](area.searchArea);
      way["building"="fire_station"](area.searchArea);
      way["building"="government"](area.searchArea);
      way["building"="toilets"](area.searchArea);
      way["building"="train_station"](area.searchArea);
      way["building"="transportation"](area.searchArea);
      way["building"="kindergarten"](area.searchArea);
      way["building"="school"](area.searchArea);
      way["building"="university"](area.searchArea);
      way["building"="college"](area.searchArea);
      way["building"="military"](area.searchArea);
      way["building"="yes"]["amenity"="college"](area.searchArea);
      way["building"="yes"]["amenity"="kindergarten"](area.searchArea);
      way["building"="yes"]["amenity"="library"](area.searchArea);
      way["building"="yes"]["amenity"="school"](area.searchArea);
      way["building"="yes"]["amenity"="university"](area.searchArea);
      way["building"="yes"]["amenity"="arts_centre"](area.searchArea);
      way["building"="yes"]["amenity"="community_centre"](area.searchArea);
      way["building"="yes"]["amenity"="theatre"](area.searchArea);
      way["building"="yes"]["amenity"="courthouse"](area.searchArea);
      way["building"="yes"]["amenity"="fire_station"](area.searchArea);
      way["building"="yes"]["amenity"="police"](area.searchArea);
      way["building"="yes"]["amenity"="prison"](area.searchArea);
      way["building"="yes"]["amenity"="ranger_station"](area.searchArea);
      way["building"="yes"]["amenity"="townhall"](area.searchArea);
      way["building"="yes"]["amenity"="toilets"](area.searchArea);
    );
    out body;
    >;
    out skel qt;
    """
    data = requests.get(URL + QUERY)
    return data

def parseData(path,data):
    nJson = data.content.decode('utf8')#.replace("'", '"')
    data = json.loads(nJson)
    buildings = []
    nodes = []

    for element in data['elements']:
        if element['type'] == "way": 
            buildings.append(element)
            continue
        nodes.append(element)
        
    for building in buildings:
        for node in nodes:
            if node['id'] == building['nodes'][0]:
                building['lat'] = node['lat']
                building['lon'] = node['lon']
                break

        public_buildings = []
        a_security =["fire_station","police"]
        a_kindergarten =["kindergarten"]
        a_school=["school","university","college"]

    for building in buildings:
        public_building = {}
        if 'name' in building['tags']:
            public_building['name'] = building['tags']['name']
        else:
            public_building['name'] = ""

        if 'addr:city' in building['tags'] and 'addr:street' in building['tags'] and 'addr:housenumber' in building['tags'] and 'addr:postcode' in building['tags']:
            public_building['address'] = building['tags']['addr:street'] + " " + building['tags']['addr:housenumber'] + ", " +building['tags']['addr:postcode'] + " " + building['tags']['addr:city']
        else:
            public_building['address'] = ""

        if 'lat' in building and 'lon' in building:
            public_building['coordinates'] = [building['lat'],building['lon']]
        else:
            public_building['coordinates'] = ""

        if 'amenity' in building['tags']:
            if building['tags']['amenity'] in a_security:
                public_building['type'] = "security"
            elif building['tags']['amenity'] in a_kindergarten:
                public_building['type'] = "kindergarten"
            elif building['tags']['amenity'] in a_school:
                public_building['type'] = "schooling"
        else:
            public_building['type'] = "government"
        public_buildings.append(public_building)
        with open(path + 'public_buildings/' + city + '.json', 'w') as fout:
            json.dump(public_buildings , fout)
        
def getOSMData(path):
    files = list_files(path + "/potential/")
    for file in files:
        city = file[:file.find(".")]
        print("Current City: " + city)
        print("Fetching Data...")
        data = getData(city)
        if data.status_code == 504 or data.status_code == 429:
            print("Error fetching Data...")
            print("Waiting for 1 Minute then trying again")
            time.sleep(60)
            data = getData(city)
        if data.status_code == 504 or data.status_code == 429:
            print("Error fetching Data...")
            print("Waiting for 5 Minutes then trying again")
            time.sleep(300)
            data = getData(city)
        if data.status_code == 504 or data.status_code == 429:  
            print("Another Error... Quitting.")
            break
            
        print("Parsing Data...")
        parseData(path,data)
    print(city + " finished!")