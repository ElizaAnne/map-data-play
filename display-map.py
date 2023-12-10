from datetime import datetime
import geopandas as gpd
import folium
import pandas as pd

# Read the GeoJSON file
file_path = 'data/footpaths.geojson'
gdf = gpd.read_file(file_path)

# retrieve sample (speeds up example)
gdf = gdf.sample(1000) 

# reproject geometries to CRS (Co-Ordinate Reference System)
# https://www.earthdatascience.org/courses/earth-analytics/spatial-data-r/intro-to-coordinate-reference-systems/
gdf = gdf.to_crs(3857)

datetime_columns = ['created_da', 'last_edi_1']

# format/impute last_edi_1 timetstamp field
for column in datetime_columns:
    gdf[column] = gdf[column].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, pd.Timestamp) else x)

# Create a map centered around the data
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=10)

# Add GeoJSON data to the map
folium.GeoJson(gdf).add_to(m)

# Display the map
m.save('map.html')  # Save the map as an HTML file
m  # Display the map in Jupyter Notebook or Colab