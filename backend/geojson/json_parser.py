import json
import os
import pathlib


def list_files():
    current_path = pathlib.Path(__file__).parent.absolute() / "potential"
    files = os.listdir(current_path)

    for file in files.copy():
        if not file.endswith(".json"):
            files.remove(file)

    #print(files)
    return files


def parse(files):
    print("Beginne mit dem Einlesen der JSON-Files")

    for file in files:
        with open("potential/" + file, 'r') as json_file:
            data=json_file.read()

        city = file[:file.find("_")]
        print("Aktuelle Stadt: " + city)

        # parse file
        obj = json.loads(data)

        buildings = obj["features"]

        for feature in buildings:
            feature["geometry"].pop("coordinates")
            feature["geometry"].pop("type")

            for property in feature["properties"].copy():
                if property == "kwh_kwp":
                    continue
                if property == "radabs":
                    continue
                if property == "anzahl_0":
                    continue
                if property == "kw_17":
                    continue
                if property == "str_17":
                    continue
                if property == "modarea":
                    continue
                feature["properties"].pop(property)

        print("JSON-File eingelesen")

        gov_buildings = get_gov_buildings(city)
        combined_buildings = []

        for gov_building in gov_buildings:
            combined_building = combine_building(gov_building, buildings)
            #print(combined_building)
            if len(combined_building) != 0:
                #print(combined_building)
                combined_buildings.append(combined_building)

        # Serializing json 
        json_object = json.dumps(combined_buildings, ensure_ascii=False)
    
        # Writing to sample.json
        filename = "../response_" + city + ".json"
        with open(filename, "w") as outfile:
            outfile.write(json_object)


def get_gov_buildings(city_name):
    filename = "public_buildings/" +  city_name + "_public_buildings.json"
    with open(filename, 'r') as json_file:
        data=json_file.read()

    gov_buildings = json.loads(data)
    return gov_buildings


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
        if "bbox" in building["geometry"]:
            if is_in_bbox(coordinates, building["geometry"]["bbox"]):
                if "type" in gov_building:
                    combine_building = {"name": gov_building["name"], "address" : gov_building["address"], "type" : gov_building["type"]}
                else:
                    combine_building = {"name": gov_building["name"], "address" : gov_building["address"], "type" : "government"}
                combine_building.update(building["properties"])
                break

    return combine_building


if __name__ == "__main__":
    files = list_files()
    parse(files)