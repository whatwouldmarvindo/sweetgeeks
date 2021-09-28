import requests

def buildStatistic(cityName):
    statistics = {}
    statistics.append(getBuildings(cityName))
    statistics.append(getProperties(cityName))
    return statistics


def getBuildings(cityName):
    buildings = {}
    return buildings

def getProperties(cityName):
    properties = {}
    return properties