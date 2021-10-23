import pandas as pd
import geopandas as gp
import json
import sys
import os
import pathlib
#import matplotlib as mp
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def list_files(path,format):
    current_path = pathlib.Path(path)
    files = os.listdir(current_path)

    for file in files.copy():
        if not file.endswith(format):
            files.remove(file)

    print(files)
    return files




def generate_bbox(coordinates):
    x=[]
    y=[]
    for thing in coordinates:
        for coordinate in thing:
            x.append(coordinate[0])
            y.append(coordinate[1])
    
    xx = sorted(x)
    yy = sorted(y)

    xMin = xx[0]
    yMin = yy[0]
    xMax = xx[len(xx)-1]
    yMax = yy[len(yy)-1]

    bbox = [xMin,yMin,xMax,yMax]
    #print(bbox)
    return bbox

def get_gov_buildings(city_name,pbPath):
    filename = pbPath +  city_name + ".json"
    with open(filename, 'r') as json_file:
        data=json_file.read()

    gov_buildings = json.loads(data)
    return gov_buildings


def is_in_bbox(coordinates, bbox):
    if(type(bbox[0]) == list):
        #bbox = bbox[0]
        # Idee: thing[0] = Gegebene bbox
        # Dann: generateBbox(thing)
        thing = []
        thing.append(bbox) 
        bbox = generate_bbox(thing)
        '''
        print("is_in_bbox_call: ")
        print(coordinates[0])
        print(type(coordinates[0]))
        print(bbox)
        print(type(bbox))
        print(bbox[0])
        print(type(bbox[0]))
        print(bbox[1])
        print(type(bbox[1]))
        print(bbox[2])
        print(type(bbox[2]))
        '''
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

def generateResponses(inPath,outPath,pbPath):
    files = list_files(inPath,".json")

    

    #file="neuss.json"
    
    for file in files:
        print("Lese JSON Datei ein")
        with open(inPath  + file, 'r') as json_file:
                    data=json_file.read()

        city = file[:file.find(".")]
        print("Aktuelle Stadt: " + city)

    # parse file
        obj = json.loads(data)

        buildings = obj["features"]

        for feature in buildings:
            #print("Geometry:\n")
            #print(feature["geometry"])
            #print("\n")
            feature["geometry"]["bbox"] = generate_bbox(feature["geometry"]["coordinates"])
            #print("BBOX:\n")
            #print(feature["geometry"]["bbox"])
            #print("\n")
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

        ################################################

        gov_buildings = get_gov_buildings(city,pbPath)
        combined_buildings = []

        for gov_building in gov_buildings:
            combined_building = combine_building(gov_building, buildings)
            #print(combined_building)
            if len(combined_building) != 0:
                #print(combined_building)
                combined_buildings.append(combined_building)

        # Serializing json
        json_object = json.dumps(combined_buildings)

        # Writing to sample.json
        filename = outPath + "response_" + city + ".json"
        with open(filename, "w", encoding="utf8") as outfile:
            outfile.write(json_object)
        print(city + " abgschlossen.")

    print("Prozedur ageschlossen.")
