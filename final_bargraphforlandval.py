from imports import pd, np, plt  # using modules from imports.py
import matplotlib.colors as mcolors
import seaborn as sns
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
SUlat, SUlong = 43.0415, -76.1363  # SU Main Campus coordinates

# Custom Distance Function 
def get_distance(lat, lon, SUlat=SUlat, SUlong=SUlong):
    SUcd = (radians(SUlat), radians(SUlong))
    objcd = (radians(lat), radians(lon))
    a = sin((SUcd[0] - objcd[0]) / 2)**2 + cos(objcd[0]) * cos(SUcd[0]) * sin((SUcd[1] - objcd[1]) / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(3963 * c, 2)

# Calculate Distance for Each Parcel
parcelFile["distance"] = parcelFile.apply(lambda row: get_distance(row["latitude"], row["longitude"]), axis=1)

# Ensure there is an 'acres' column; filter out rows where acres is zero to avoid division by zero.
if 'acres' not in parcelFile.columns:
    raise ValueError("The CSV file must include an 'acres' column.")
parcelFile = parcelFile[parcelFile['acres'] > 0]

# Calculate land value per acre using the formula: land_av / acres
parcelFile['land_value_per_acre'] = parcelFile['land_av'] / parcelFile['acres']

# Filter parcels within 0-5 miles of SU
df_filtered = parcelFile[(parcelFile["distance"] >= 0) & (parcelFile["distance"] <= 5)]
print("Number of parcels within 0-5 miles:", len(df_filtered))

# Create bins (0.5-mile intervals)
bins = np.arange(0, 5.5, 0.5)
df_filtered["distance_bin"] = pd.cut(df_filtered["distance"], bins=bins)

# Calculate average land value per acre per bin and count per bin
avg_values = df_filtered.groupby("distance_bin", observed=True).agg({
    "land_value_per_acre": "mean", 
    "distance": "count"
}).reset_index().rename(columns={"distance": "count"})
avg_values["distance_mid"] = avg_values["distance_bin"].apply(lambda x: x.left + (x.right - x.left) / 2)
print("Average values per bin:\n", avg_values)

# Normalize the counts to [0,1] for color mapping.
min_count = avg_values['count'].min()
max_count = avg_values['count'].max()
if max_count > min_count:
    avg_values['norm_count'] = (avg_values['count'] - min_count) / (max_count - min_count)
else:
    avg_values['norm_count'] = 0.5


'''
https://facelessuser.github.io/coloraide/interpolation/
'''
# Define a function to interpolate between a "light" and a "base" hex color.
# When norm is 0, return light_hex; when norm is 1, return base_hex.
def interpolate_color(value, base_hex, light_hex):
    base_rgb = mcolors.to_rgb(base_hex)
    light_rgb = mcolors.to_rgb(light_hex)
    r = light_rgb[0] * (1 - value) + base_rgb[0] * value
    g = light_rgb[1] * (1 - value) + base_rgb[1] * value
    b = light_rgb[2] * (1 - value) + base_rgb[2] * value
    return mcolors.to_hex((r, g, b))

# Set base color and light color.
base_hex = "#0000FF"   # Pure blue
light_hex = "#BBBBFF"  # light blue

# Generate a list of hex colors for each bin based on normalized count.
colors_list = [interpolate_color(val, base_hex, light_hex) for val in avg_values['norm_count']]

'''
https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
'''
# Plotting: Bar Graph (Distance vs. Average Land Value per Acre)
plt.figure(figsize=(10, 6))
sns.barplot(x="distance_mid", y="land_value_per_acre", data=avg_values, palette=colors_list)
plt.xlabel("Distance from SU (miles)")
plt.ylabel("Average Land Value per Acre (USD/acre)")
plt.title("Distance vs. Average Land Value per Acre (0-5 miles)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
