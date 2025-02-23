from imports import plt, sns, pd, np
from matplotlib.ticker import FuncFormatter
import data

# Creating the land val bar plot
# Calculate Distance for Each Parcel
parcelDistances = [data.properties[i].getDistance() for i in range(data.parcelLength)]

# Create bins ()
bins = np.arange(0, int(max(parcelDistances)+0.5), 0.5)
bardf = pd.DataFrame()
bardf["bin"] = pd.cut(parcelDistances, bins=bins)
bardf["val"] = [data.parcelLandVal[i]/data.parcelAcre[i] for i in range(data.parcelLength)]

# Calculate average land per acre value (from data.parcelLandVal) per bin
avgs = bardf.groupby("bin", observed=False).mean().reset_index()
avgs["label"] = avgs["bin"].apply(lambda x: x.left + (x.right - x.left) / 2)

# Plotting: Bar Graph (Distance vs. Average Land Value)
plt.figure(figsize=(10, 6))
sns.barplot(x="label", y="val", data=avgs, palette="coolwarm", hue="label", legend=False)
plt.xlabel("Distance from SU (miles)")
plt.ylabel("Average Land Value per Acre (USD/Acre)")
plt.title("Distance from SU vs. Average Land Value per Acre")
plt.xticks(rotation=45)
plt.tight_layout()
plt.gca().yaxis.set_major_formatter(FuncFormatter('${:,.0f}'.format))
plt.savefig("landValAcreBarGraph") # Saving the land graph to use

# Creating the property val bar plot
bardf["value"] = [data.parcelPropertyVal[i]/data.parcelAcre[i] for i in range(data.parcelLength)]

# Calculate average property per acre value (from data.parcelPropertyVal) per bin
avgs = bardf.groupby("bin", observed=False).mean().reset_index()
avgs["label"] = avgs["bin"].apply(lambda x: x.left + (x.right - x.left) / 2)

# Plotting: Bar Graph (Distance vs. Average Property Value)
plt.figure(figsize=(10, 6))
sns.barplot(x="label", y="value", data=avgs, palette="coolwarm", hue="label", legend=False)
plt.xlabel("Distance from SU (miles)")
plt.ylabel("Average Property Value per Acre (USD/Acre)")
plt.title("Distance from SU vs. Average Property Value per Acre")
plt.xticks(rotation=45)
plt.tight_layout()
plt.gca().yaxis.set_major_formatter(FuncFormatter('${:,.0f}'.format))
plt.savefig("propValAcreBarGraph") # Saving the property graph to use

# Showing the graphs
plt.show()