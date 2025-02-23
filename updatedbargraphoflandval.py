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

# Calculate average land value per acre per bin
avg_values = df_filtered.groupby("distance_bin", observed=True).agg({"land_value_per_acre": "mean"}).reset_index()
avg_values["distance_mid"] = avg_values["distance_bin"].apply(lambda x: x.left + (x.right - x.left) / 2)
print("Average values per bin:\n", avg_values)

# Plotting: Bar Graph (Distance vs. Average Land Value per Acre)
plt.figure(figsize=(10, 6))
sns.barplot(x="distance_mid", y="land_value_per_acre", data=avg_values, palette="coolwarm")
plt.xlabel("Distance from SU (miles)")
plt.ylabel("Average Land Value per Acre (USD/acre)")
plt.title("Distance vs. Average Land Value per Acre (0-5 miles)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
