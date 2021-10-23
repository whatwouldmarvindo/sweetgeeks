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



def generateDatabaseInserts(inPath,outPath):
    files = list_files(inPath,".json")
    output = ""
    for file in files:
        print("Lese JSON Datei ein")
        with open(inPath  + file, 'r') as json_file:
                    data=json_file.read()

        city = file[:file.find(".json")]
        print("Aktuelle Stadt: " + city)

        obj = json.loads(data)
        print("Generiere Queries")
        for building in obj:
            name = building["name"].replace("'","")
            address = building["address"].replace("'","")
            type = building["type"].replace("'","")
            modarea = building["modarea"]
            radabs = building["radabs"]
            kwh_kwp = building["kwh_kwp"]
            anzahl_0 = building["anzahl_0"]
            kw_17 = building["kw_17"]
            str_17 = building["str_17"]
            query = "INSERT INTO Gebaeude(StadtID,name,address,type,modarea,radabs,kwh_kwp,anzahl_0,kw_17,str_17) VALUES ((Select StadtID from Staedte where Staedte.Name = '"+str(city)+"'), '"+str(name)+"', '"+str(address)+"', '"+str(type)+"', "+str(modarea)+", "+str(radabs)+", "+str(kwh_kwp)+", "+str(anzahl_0)+", "+str(kw_17)+", "+str(str_17)+");"
            output = output + query + "\n"
    return output

def generateSQLScript(inPath,outPath):
    out = generateDatabaseInserts(inPath,outPath)
    filename = outPath + "gebaeudeInserts"+ ".sql"
    with open(filename, "w", encoding="utf8") as outfile:
        outfile.write(out)