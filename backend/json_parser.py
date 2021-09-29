import json


def parse():
    print("Beginne mit dem Einlesen des JSON-Files")
    with open('grevenbroich_solar.json', 'r') as myfile:
        data=myfile.read()

    # parse file
    obj = json.loads(data)

    features = obj["features"]
    
    for feature in features:
        feature["geometry"].pop("coordinates")
        feature["geometry"].pop("type")

        properties = feature["properties"].copy()
        for property in properties:
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


    # Serializing json 
    json_object = json.dumps(features)
  
    # Writing to sample.json
    with open("short_gv_solar.json", "w") as outfile:
        outfile.write(json_object)



if __name__ == "__main__":
    parse