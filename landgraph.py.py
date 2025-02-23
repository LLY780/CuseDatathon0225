import pandas as pd
import numpy as np
from math import sin, cos, atan2, sqrt, radians
import matplotlib.pyplot as plt
import seaborn as sns

# directory paths
base_path = "C:/Users/sajid/CuseDatathon0225/CuseDatathon0225/"
parcel_csv = base_path + "Syracuse_Parcel_Map_(Q4_2024).csv"

# Data preparation
parcelFile = pd.read_csv(parcel_csv)
parcelFile.columns = parcelFile.columns.str.lower()  

# Rename coordinate columns:
if "lat" in parcelFile.columns and "latitude" not in parcelFile.columns:
    parcelFile = parcelFile.rename(columns={"lat": "latitude"})
if "long" in parcelFile.columns and "longitude" not in parcelFile.columns:
    parcelFile = parcelFile.rename(columns={"long": "longitude"})

# Syracuse University Coordinates
SUlat, SUlong = 43.0415, -76.1363  # SU Main Campus coordinates

# Custom Distance Function 
def get_distance(lat, lon, SUlat=SUlat, SUlong=SUlong):
    SUcd = (radians(SUlat), radians(SUlong))
    objcd = (radians(lat), radians(lon))
    a = sin((SUcd[0] - objcd[0]) / 2)**2 + cos(objcd[0]) * cos(SUcd[0]) * sin((SUcd[1] - objcd[1]) / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 3963 * c  # Earth's radius in miles
    return round(distance, 2)

# Calculate Distance for Each Parcel
parcelFile["distance"] = parcelFile.apply(lambda row: get_distance(row["latitude"], row["longitude"]), axis=1)

# Filter parcels within 0-5 miles of SU
df_filtered = parcelFile[(parcelFile["distance"] >= 0) & (parcelFile["distance"] <= 5)]

# Create bins (0.5-mile intervals)
bins = np.arange(0, 5.5, 0.5)
df_filtered["distance_bin"] = pd.cut(df_filtered["distance"], bins=bins)

# Calculate average land value (from column "land_av") per bin
avg_values = df_filtered.groupby("distance_bin").agg({"land_av": "mean"}).reset_index()
avg_values["distance_mid"] = avg_values["distance_bin"].apply(lambda x: x.left + (x.right - x.left) / 2)

# Plotting: Bar Graph (Distance vs. Average Land Value)
plt.figure(figsize=(10, 6))
sns.barplot(x="distance_mid", y="land_av", data=avg_values, palette="coolwarm")
plt.xlabel("Distance from SU (miles)")
plt.ylabel("Average Land Value")
plt.title("Distance vs. Average Land Value (0-5 miles)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()