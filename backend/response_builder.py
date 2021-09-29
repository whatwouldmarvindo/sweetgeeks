import json


def build_statistic(cityName):
    filename = "response_" + cityName + ".json"
    with open(filename, 'r') as myfile:
        data=myfile.read()

    # parse file
    response = json.loads(data)
    return response