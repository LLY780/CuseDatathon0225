import data
from imports import pd, np, plt
import matplotlib.colors as mcolors

# Directory paths
parcel_csv = "Syracuse_Parcel_Map_(Q4_2024).csv"

# Data preparation
parcelFile = pd.read_csv(parcel_csv)
parcelFile.columns = parcelFile.columns.str.lower()
parcelFile.rename(columns={"lat": "latitude", "long": "longitude"}, inplace=True)

# Ensure 'acres' column exists:
if 'acres' not in parcelFile.columns:
    raise ValueError("The CSV must contain an 'acres' column for acreage.")

# Calculate land value per acre = land_av / acres
parcelFile['land_value_per_acre'] = parcelFile['land_av'] / parcelFile['acres']

# Define fixed bins for land value per acre (USD/acre)
# For example: Bin 1: 0 - 5,000; Bin 2: 5,000 - 10,000; Bin 3: 10,000 - 15,000; Bin 4: 15,000+
boundaries = [0, 250000, 500000, 750000, 1e9]

# Define color palette (4 colors)
colors = [
    "#A020F0",  # Purple for 0 - $250K/acre
    "#0000FF",  # Blue for $250K - $500K/acre
    "#00FF00",  # Green for $500K - $750K/acre
    "#FFA500"  # Orange for >$750K/acre
]
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(boundaries, cmap.N)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(parcelFile['longitude'], parcelFile['latitude'],
                      c=parcelFile['land_value_per_acre'], cmap=cmap, norm=norm,
                      alpha=0.7, edgecolor='k')

tick_locs = [(boundaries[i] + boundaries[i+1]) / 2 for i in range(len(boundaries)-1)]
cbar = plt.colorbar(scatter, ticks=tick_locs)
cbar.ax.set_yticklabels([
    f"${boundaries[0]//1000:.0f}K - ${boundaries[1]//1000:.0f}K",
    f"${boundaries[1]//1000:.0f}K - ${boundaries[2]//1000:.0f}K",
    f"${boundaries[2]//1000:.0f}K - ${boundaries[3]//1000:.0f}K",
    f">${boundaries[3]//1000:.0f}K"
])
cbar.set_label('Land Value per Acre (USD/acre)')

# Mark Syracuse University on the map.
SUlat, SUlong = 43.0366, -76.1338  # SU Main Campus
plt.scatter(SUlong, SUlat, color='red', marker='*', s=200, label='Syracuse University')

plt.title('Topological Map: Land Value per Acre')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.savefig("landValAcreTopoGraph")

# Calculate property value per acre = (total_av - land_av) / acres
df = pd.DataFrame({"prop_av":data.parcelPropertyVal})
parcelFile['property_value_per_acre'] = (parcelFile['total_av'] - parcelFile['land_av']) / parcelFile['acres']

plt.figure(figsize=(10, 8))
scatter = plt.scatter(parcelFile['longitude'], parcelFile['latitude'],
                      c=parcelFile['property_value_per_acre'], cmap=cmap, norm=norm,
                      alpha=0.7, edgecolor='k')

# Configure colorbar with tick labels at bin midpoints.
tick_locs = [(boundaries[i] + boundaries[i+1]) / 2 for i in range(len(boundaries)-1)]
cbar = plt.colorbar(scatter, ticks=tick_locs)
cbar.ax.set_yticklabels([
    f"${boundaries[0]//1000:.0f}K - ${boundaries[1]//1000:.0f}K",
    f"${boundaries[1]//1000:.0f}K - ${boundaries[2]//1000:.0f}K",
    f"${boundaries[2]//1000:.0f}K - ${boundaries[3]//1000:.0f}K",
    f">${boundaries[3]//1000:.0f}K"
])
cbar.set_label('Property Value per Acre (USD/acre)')

# Mark Syracuse University on the map (optional; update coordinates as needed)
plt.scatter(data.SUParcel["LONG"], data.SUParcel["LAT"], color='red', marker='*', s=200, label='Syracuse University')
plt.title('Topological Map: Property Value per Acre')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.savefig("propValAcreTopoGraph")

# Showing the graphs
plt.show()