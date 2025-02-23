from imports import plt, np, pd
import matplotlib.colors as mcolors
import data

# Calculate distance from Syracuse University for each parcel
parcelDistances = [data.properties[i].getDistance() for i in range(data.parcelLength)]

# Define a list of 4 colors.
colors = [
    "#A020F0",  # Purple for 0 - $250K/acre
    "#0000FF",  # Blue for $250K - $500K/acre
    "#00FF00",  # Green for $500K - $750K/acre
    "#FFA500"  # Orange for >$750K/acre
]
cmap = mcolors.ListedColormap(colors)

# Creating choropleth map for distance from campus
# Define boundaries for bins: 0-1, 1-2, 2-3, 3-4 miles.
bounds = np.arange(0, max(parcelDistances)+1, 1.0)  # [0, 1, 2, 3, 4]

# Plotting the parcels through GeoPandas
data.parcelgdf["val"] = parcelDistances

tick_locs = [(bounds[i] + bounds[i+1]) / 2 for i in range(len(bounds)-1)]
def tick_dist(x, pos):
    for i in range(len(bounds)-1):
        if bounds[i] <= x <= bounds[i+1]:
            return f"{bounds[i]}-{bounds[i+1]} miles"

data.parcelgdf.plot(cmap=cmap, column="val", legend=True, legend_kwds={"ticks":tick_locs,"label":'Distance from SU (miles)',"format":tick_dist})

# Mark Syracuse  University on the map.
plt.scatter(data.SUParcel["LONG"], data.SUParcel["LAT"], color='red', marker='*', s=200, label='Syracuse University')
plt.title('Parcel Map: Discrete Proximity to Syracuse University')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.savefig("distanceCplethGraph")

# Showing the graph
plt.show()
