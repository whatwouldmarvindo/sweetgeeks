import json

buildings = dict()

def get_gov_buildings():
    with open('public_buildings_GV.json', 'r') as myfile:
        data=myfile.read()

    gov_buildings = json.loads(data)
    return gov_buildings


def create_response(gov_buildings):
    with open('short_gv_solar.json', 'r') as myfile:
        data=myfile.read()

    response_list = []
    buildings = json.loads(data)

    for gov_building in gov_buildings:
        combined_building = combine_building(gov_building, buildings)
        if len(combined_building) != 0:
            #print(combined_building)
            response_list.append(combined_building)

    print(response_list)
    return response_list

def is_in_bbox(coordinates, bbox):
    if coordinates[1] >= bbox[0] and coordinates[1] <= bbox[2]:
        if coordinates[0] >= bbox[1] and coordinates[0] <= bbox[3]:
            #print("Building found")
            return True
    #print("Building not found - WARNING")
    return False


def combine_building(gov_building, buildings):
    coordinates = gov_building["coordinates"]

    combine_building = {}

    for building in buildings:
        if is_in_bbox(coordinates, building["geometry"]["bbox"]):
            if "type" in gov_building:
                combine_building = {"name": gov_building["name"], "address" : gov_building["address"], "type" : gov_building["type"]}
            else:
                combine_building = {"name": gov_building["name"], "address" : gov_building["address"], "type" : "government"}
            combine_building.update(building["properties"])
            break

    return combine_building


if __name__ == "__main__":
    gov_buildings = get_gov_buildings()
    response = create_response(gov_buildings)

     # Serializing json 
    json_object = json.dumps(response)
  
    # Writing to sample.json
    with open("response_grevenbroich.json", "w") as outfile:
        outfile.write(json_object)