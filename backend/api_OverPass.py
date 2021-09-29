import json
import requests

def query(city):
    URL = "https://overpass-api.de/api/interpreter?data="
    QUERY = """
    [out:json];
    area[name="{city}"]->.searchArea;
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

def getBuildings(city):
    data = query(city)
    nJson = data.content.decode('utf8').replace("'", '"')
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
        
    return public_buildings