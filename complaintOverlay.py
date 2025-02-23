from imports import gpd
from imports import plt

polygon_file = 'Syracuse_Parcel_Map_(Q4_2024).geojson'
point_file = 'SYRCityline_Requests_(2021-Present).geojson'
output_file = 'combined.geojson'

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

gdf1 = gpd.read_file(polygon_file)
gdf2 = gpd.read_file(point_file)

gdf1.plot(ax=ax, color='blue')
gdf2.plot(ax=ax, color='orange')
plt.show()

