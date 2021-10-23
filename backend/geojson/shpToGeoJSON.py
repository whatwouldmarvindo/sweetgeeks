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

def generateGeoJSON(inPath,outPath):
    files = list_files(inPath,".zip")
    
    for file in files:
        city = file[:file.find(".")]
        print("Current City: " + city )
        zipfile = "zip://" + inPath + file
        gdf = gp.read_file(zipfile, encoding="latin")
        gdf = gdf.to_crs("EPSG:4326")
        print("Processing finished, writing to file...")
        gdf.to_file(outPath + "potential/" + city + ".json", driver='GeoJSON')
        print(city + " finished!" + "\n")
    print("Job's done!")

    