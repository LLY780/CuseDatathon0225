from imports import pd
from imports import plt
from Property import Property

parcelFile = pd.read_csv("Syracuse_Parcel_Map_(Q4_2024).csv")
cityFile = pd.read_csv("SYRCityline_Requests_(2021-Present).csv")

# parcelFile columns
parcelAddress = list(parcelFile["FullAddres"])
parcelAdditionalAddress = list(parcelFile["Add2_OwnSt"])
parcelLandVal = list(parcelFile["land_av"])
parcelTotalVal = list(parcelFile["total_av"])
parcelOwner = list(parcelFile["Owner"])
parcelCondition = list(parcelFile["IPS_Condit"])
parcelLatitude = list(parcelFile["LAT"])
parcelLongitude = list(parcelFile["LONG"])
SUParcel = parcelFile.iloc[18182]

# cityFile columns
cityCategory = list(cityFile["Category"])
cityAddress = list(cityFile["Address"])
cityLatitude = list(cityFile["Lat"])
cityLongitude = list(cityFile["Lng"])

# custom columns
parcelPropertyVal = [parcelTotalVal[i]-parcelLandVal[i] for i in range(len(parcelTotalVal))]

# list of all parcels using Property class
properties = [Property(parcelAddress[i],parcelLandVal[i],parcelPropertyVal[i],parcelLatitude[i],parcelLongitude[i]) for i in range(len(parcelTotalVal))]
