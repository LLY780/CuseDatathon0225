import pandas as pd

parcelFile = pd.read_csv("Syracuse_Parcel_Map_(Q4_2024).csv")
cityFile = pd.read_csv("SYRCityline_Requests_(2021-Present).csv")

#parcelFile columns
parcelAddress = list(parcelFile["FullAddres"])
parcelAdditionalAddress = list(parcelFile["Add2_OwnSt"])
parcelLandVal = list(parcelFile["land_av"])
parcelTotalVal = list(parcelFile["total_av"])
parcelOwner = list(parcelFile["Owner"])
parcelCondition = list(parcelFile["IPS_Condit"])
parcelLatitude = list(parcelFile["LAT"])
parcelLongitude = list(parcelFile["LONG"])
SUParcel = parcelFile.iloc[18182]

#cityFile columns
cityCategory = cityFile["Category"]
cityAddress = cityFile["Category"]

#creating custom columns
parcelPropertyVal = []
for i in range(len(parcelTotalVal)):
    parcelPropertyVal.append(parcelTotalVal[i]-parcelLandVal[i])
