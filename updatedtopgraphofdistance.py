import pandas as pd
import numpy as np
from math import sin, cos, atan2, sqrt, radians
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Directory paths
base_path = "C:/Users/sajid/CuseDatathon0225/CuseDatathon0225/"
parcel_csv = base_path + "Syracuse_Parcel_Map_(Q4_2024).csv"

# Data preparation
parcelFile = pd.read_csv(parcel_csv)
parcelFile.columns = parcelFile.columns.str.lower()  

# Rename coordinate columns if necessary
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

# Calculate distance from Syracuse University for each parcel
parcelFile['distance'] = parcelFile.apply(lambda row: get_distance(row['latitude'], row['longitude']), axis=1)

# Define boundaries for bins: 0-1, 1-2, 2-3, 3-4 miles.
bounds = np.arange(0, 4.0 + 1, 1.0)  # [0, 1, 2, 3, 4]

# Define a list of 4 colors. 
colors = [
    "#EE8434",  # 0 - 1 miles: 
    "#717EC3",  # 1 - 2 miles: 
    "#AE8799",  # 2 - 3 miles: 
    "#C95D63"   # 3 - 4 miles: 
]
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(bounds, cmap.N)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(parcelFile['longitude'], parcelFile['latitude'], 
                      c=parcelFile['distance'], cmap=cmap, norm=norm,
                      alpha=0.7, edgecolor='k')

# Configure the colorbar to show labels for each bin.
tick_locs = [(bounds[i] + bounds[i+1]) / 2 for i in range(len(bounds) - 1)]
cbar = plt.colorbar(scatter, ticks=tick_locs)
cbar.ax.set_yticklabels([f"{bounds[i]}-{bounds[i+1]} miles" for i in range(len(bounds)-1)])
cbar.set_label('Distance from SU (miles)')

# Mark Syracuse University on the map.
plt.scatter(SUlong, SUlat, color='red', marker='*', s=200, label='Syracuse University')
plt.title('Parcel Map: Discrete Proximity to Syracuse University (0-4 miles)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()
