from math import *

class Property:
    # constructor asks for, in order
    # (name of property, land value, propertyValue, latitude, longitude)
    def __init__(self,address,landValue,propertyValue,objLat, objLong):
        self.landValue = landValue
        self.propertyValue = propertyValue
        self.address = address
        self.objLong = objLong
        self.objLat = objLat

    #SU's longitude and latitude
    global SUlong
    SUlong = -76.13553411
    global SUlat
    SUlat = 43.03465908

    # get funcs
    def getAddress(self): # returns name of property
        return self.address
    def getLandValue(self): # returns land value
        return self.landValue
    def getPropertyValue(self): # returns property value
        return self.propertyValue
    def getObjLong(self): # returns longitude
        return self.objLong
    def getObjLat(self): # returns latitude
        return self.objLat
    def getQuality(self): # returns Quality
        return self.propertyValue - self.landValue
    def getDistance(self): # returns distance to SU
        #uses halvorsines formula
        SUcd = (radians(SUlat),radians(SUlong))
        objcd = (radians(self.objLat), radians(self.objLong))
        a = sin((SUcd[0]-objcd[0])/2)**2 + cos(objcd[0]) * cos(SUcd[0]) * sin((SUcd[1]-objcd[1])/2)**2
        c = 2 * atan2(sqrt(a),sqrt(1-a))
        distance = 3963 * c
        return round(distance,2)

    def __str__(self): # string representation
        return "Property: " + self.address + " | Distance from SU: " + str(self.getDistance()) + "mi | Land Value: $" + str(self.landValue) + " | Property Value: $" + str(self.propertyValue) + " | Quality $" + str(self.getQuality()) + " | Latitude "+ str(self.objLat) + " | Longitude "+ str(self.objLong)

    def __repr__(self):
        return "(Property " + self.address + " | Distance from SU " + str(self.getDistance()) + " | Land Value: $" + str(
            self.landValue) + " | Property Value: $" + str(self.propertyValue) + " | Quality $" + str(
            self.getQuality()) + " | Latitude " + str(self.objLat) + " | Longitude " + str(self.objLong) +")"
