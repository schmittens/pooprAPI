from math import pi, cos

def calculateBounds(lon, lat, rad):
    lon = round(float(lon), 6)
    lat = round(float(lat), 6)

    lowerLon = lon - (180 / pi) * (rad / 6378137) / cos(lat)
    upperLon = lon + (180 / pi) * (rad / 6378137) / cos(lat)
    lowerLat = lat - (180 / pi) * (rad / 6378137) #/ cos(lat)
    upperLat = lat + (180 / pi) * (rad / 6378137) #/ cos(lat)

    if lowerLon > upperLon:
        print("switching lon")
        lowerLon, upperLon = upperLon, lowerLon

    if lowerLat > upperLat:
        print("switching lat")
        lowerLat, upperLat = upperLat, lowerLat

    returnDict = {"lowerLon": lowerLon, "upperLon": upperLon, "lowerLat": lowerLat, "upperLat": upperLat}
    #print(returnDict)
    return returnDict