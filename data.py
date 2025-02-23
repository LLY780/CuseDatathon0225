from imports import pd, gpd
from Property import Property

parceldf = pd.read_csv("Syracuse_Parcel_Map_(Q4_2024).csv") # filter out blank values
citydf = pd.read_csv("SYRCityline_Requests_(2021-Present).csv")
parcelgdf = gpd.read_file("Syracuse_Parcel_Map_(Q4_2024).geojson")
citygdf = gpd.read_file("SYRCityline_Requests_(2021-Present).geojson")

parcelLength = len(parceldf)
cityLength = len(citydf)

# parceldf columns
parcelAddress = list(parceldf["FullAddres"])
parcelAdditionalAddress = list(parceldf["Add2_OwnSt"])
parcelLandVal = list(parceldf["land_av"])
parcelTotalVal = list(parceldf["total_av"])
parcelOwner = list(parceldf["Owner"])
parcelAcre = list(parceldf["ACRES"])
parcelLatitude = list(parceldf["LAT"])
parcelLongitude = list(parceldf["LONG"])
SUParcel = parceldf.loc[18178]

# citydf columns
cityCategory = list(citydf["Category"])
cityAddress = list(citydf["Address"])
cityLatitude = list(citydf["Lat"])
cityLongitude = list(citydf["Lng"])

# custom columns
parcelPropertyVal = [parcelTotalVal[i]-parcelLandVal[i] for i in range(len(parcelTotalVal))]

# list of all parcels using Property class
properties = [Property(parcelAddress[i],parcelLandVal[i],parcelPropertyVal[i],parcelLatitude[i],parcelLongitude[i]) for i in range(len(parcelTotalVal))]
