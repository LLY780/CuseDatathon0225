from data import*
from Property import*


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
    for i in range(len)


def medianLandValue():
    middle = len(parcelTotalVal) // 2
    if len(parcelTotalVal) % 2 == 0:
        return (parcelLandVal[middle]+parcelLandVal[middle+1])/2
    else:
        return parcelLandVal[middle]

def medianPropertyValue():
    middle = len(parcelTotalVal) // 2
    if len(parcelTotalVal) % 2 == 0:
        return (parcelPropertyVal[middle]+parcelPropertyVal[middle+1])/2
    else:
        return parcelPropertyVal[middle]

def medianTotalValue():
    middle = len(parcelTotalVal) // 2
    if len(parcelTotalVal) % 2 == 0:
        return (parcelTotalVal[middle]+parcelTotalVal[middle+1])/2
    else:
        return parcelTotalVal[middle]





#print(propdensity())
