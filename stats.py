from data import*
from Property import*

def searchProp(addy):
    for i in range(len(parcelTotalVal)):
        if addy == properties[i].getAddress():
            return properties[i]

    return "this property doesn't exist"

def getDistance(point1, point2):  # returns distance to SU
    # uses halvorsines formula
    cd1 = (radians(point1[0]), radians(point1[1]))
    cd2 = (radians(point2[0]), radians(point2[1]))
    a = sin((cd1[0] - cd2[0]) / 2) ** 2 + cos(cd2[0]) * cos(cd1[0]) * sin((cd1[1] - cd2[1]) / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 3963 * c
    return round(distance, 2)

def propdensity():
    bottoml = (min(parcelLatitude),min(parcelLongitude))
    bottomr = (max(parcelLatitude), min(parcelLongitude))
    topl = (min(parcelLatitude), max(parcelLongitude))
    topr = (max(parcelLatitude), max(parcelLongitude))

    area = getDistance(bottoml,bottomr) * getDistance(bottoml,topl)

    return len(parcelLongitude) / area

def propdensityrad(radius, prop): #radius in miles
    area = radius**2 * pi
    count = 0
    propcd = (prop.getObjLat(), prop.getObjLong())
    for i in range(len(parcelTotalVal)):
        if getDistance(propcd,(properties[i].getObjLat(),properties[i].getObjLong())) < radius:
            count += 1

    return count / area

def medianValue(lst):
    middle = len(parcelTotalVal) // 2
    if len(parcelTotalVal) % 2 == 0:
        return (lst[middle]+lst[middle+1])/2
    else:
        return lst[middle]

def meanValue(lst):
    sum = 0
    for i in range(len(parcelTotalVal)):
        sum += lst[i]
    return round(sum / len(parcelTotalVal),2)


# def standarddev(lst):
#     topstuff = 


print(propdensityrad(1.5,searchProp("940 COMSTOCK AVE & COLVIN ST")))
print(propdensity())
