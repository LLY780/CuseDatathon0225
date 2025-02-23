from imports import pd, np, plt  # Using modules from imports.py
import matplotlib.colors as mcolors
from math import sin, cos, atan2, sqrt, radians

# Directory paths (adjust if necessary)
base_path = "C:/Users/sajid/CuseDatathon0225/CuseDatathon0225/"
parcel_csv = base_path + "Syracuse_Parcel_Map_(Q4_2024).csv"

# Data preparation
parcelFile = pd.read_csv(parcel_csv)
parcelFile.columns = parcelFile.columns.str.lower()

# Rename coordinate columns if necessary
parcelFile.rename(columns={"lat": "latitude", "long": "longitude"}, inplace=True)

# Syracuse University Coordinates
SUlat, SUlong = 43.0366, -76.1338  # SU Main Campus

# Custom Distance Function (for reference)
def get_distance(lat, lon, SUlat=SUlat, SUlong=SUlong):
    SUcd = (radians(SUlat), radians(SUlong))
    objcd = (radians(lat), radians(lon))
    a = sin((SUcd[0] - objcd[0]) / 2) ** 2 + cos(objcd[0]) * cos(SUcd[0]) * sin((SUcd[1] - objcd[1]) / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(3963 * c, 2)

# Calculate distance for each parcel (optional, for reference)
parcelFile['distance'] = parcelFile.apply(lambda row: get_distance(row['latitude'], row['longitude']), axis=1)
parcelFile["property_value"] = parcelFile["total_av"] - parcelFile["land_av"]
parcelFile['price_per_acre'] = parcelFile['total_av'] / parcelFile['acres']

# --- Color mapping based on total_av ---
# Define fixed bin boundaries (in USD) for total_av:
# Bin 1: $0 - $250,000; Bin 2: $250,000 - $500,000; Bin 3: $500,000 - $750,000; Bin 4: $750,000+
boundaries = [0, 250000, 500000, 750000, 1e9]  # Upper cap for values above $750K

# Define the corresponding 4-color palette:
colors = [
    "#A020F0",  # Purple for $0 - $250K
    "#0000FF",  # Blue for $250K - $500K
    "#00FF00",  # Green for $500K - $750K
    "#FFA500"   # Orange for $750K+
]
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(boundaries, cmap.N)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(parcelFile['longitude'], parcelFile['latitude'],
                      c=parcelFile['price_per_acre'], cmap=cmap, norm=norm,
                      alpha=0.7, edgecolor='k')

# Configure the colorbar with tick labels at the midpoints of each bin.
tick_locs = [(boundaries[i] + boundaries[i+1]) / 2 for i in range(len(boundaries)-1)]
cbar = plt.colorbar(scatter, ticks=tick_locs)
cbar.ax.set_yticklabels([
    f"${boundaries[0]//1000:.0f}K - ${boundaries[1]//1000:.0f}K",
    f"${boundaries[1]//1000:.0f}K - ${boundaries[2]//1000:.0f}K",
    f"${boundaries[2]//1000:.0f}K - ${boundaries[3]//1000:.0f}K",
    f">${boundaries[3]//1000:.0f}K"
])
cbar.set_label('Total Value (USD)')

# Mark Syracuse University on the map.
plt.scatter(SUlong, SUlat, color='red', marker='*', s=200, label='Syracuse University')
plt.title('Parcel Map: Total Value by Price per Acre')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()
