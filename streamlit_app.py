import folium
import math
from folium import plugins
from folium.plugins import Draw

import json, re, requests
import pandas as pd

import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# Draw the original map
m = folium.Map(location=[0,0], zoom_start=2)

# Add draw feature
Draw(export=True).add_to(m)

# Draw arrow for start and end point
def draw_arrow(start_point, end_point,m):
    # Define coordinates for the line
    # start_point
    # end_point 

    # Draw a line between start and end points
    folium.PolyLine(locations=[start_point, end_point], color='blue', weight=5).add_to(m)

    # Calculate the bearing (direction) between start and end points
    delta_lon = math.radians(end_point[1] - start_point[1])
    start_lat_rad = math.radians(start_point[0])
    end_lat_rad = math.radians(end_point[0])

    y = math.sin(delta_lon) * math.cos(end_lat_rad)
    x = math.cos(start_lat_rad) * math.sin(end_lat_rad) - math.sin(start_lat_rad) * math.cos(end_lat_rad) * math.cos(delta_lon)
    bearing = math.atan2(y, x)

    # Convert bearing from radians to degrees
    bearing = math.degrees(bearing)

    # Draw a triangle marker at the end point to indicate direction
    triangle_marker = folium.RegularPolygonMarker(location=end_point, color='blue', fill_color='blue', number_of_sides=3, radius=7, rotation=bearing+30)
    triangle_marker.add_to(m)

title_column = st.container()
with title_column:
    st.title("Interactive Map of Historic Migrations")


folium.Marker([21.24842224, 105.77636719], popup='1979-1987 Vietnam Exodus 1M Displaced').add_to(m)
folium.Marker([22.17261,77.912088], popup='1947 India-Pakistan Mass Migration 10M Displaced').add_to(m)
folium.Marker([31.559353,71.409623], popup='1947 India-Pakistan Mass Migration 10M Displaced').add_to(m)


########################################################################################################################

# dynamically get the world-country boundaries 
res = requests.get("https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json")
df = pd.DataFrame(json.loads(res.content.decode()))
df = df.assign(id=df["features"].apply(pd.Series)["id"],
         name=df["features"].apply(pd.Series)["properties"].apply(pd.Series)["name"])

# build a dataframe of country colours scraped from wikipedia

########################################################################################################################

# a list of interesting countries - Singapore is missing!
countries = ["Bulgaria","Malaysia","Pakistan","Vietnam","India"]



# overlay desired countries over folium map
for r in df.loc[df["name"].isin(countries)].to_dict(orient="records"):
    folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"]).add_to(m)

########################################################################################################################

#ARROW##################################################################################################################
# Example arrow
india_coordinates = [22.17261,77.912088]
pakistan_coordinates = [31.559353,71.409623]
draw_arrow(india_coordinates,pakistan_coordinates,m)
draw_arrow(pakistan_coordinates,india_coordinates,m)


######################
# Define the radius of the circle (in meters)
radius = 1000000  # For example, 1000 km

# Create a circle object with the specified center coordinates and radius
circle = folium.Circle(location=[0,0], radius=radius, color='red', fill=True, fill_color='red', fill_opacity=0.5)

# Add the circle to the map
circle.add_to(m)
######################

# Define the coordinates that make up the border of Ohio
# china_border = 

# Draw a polygon representing the border of China
# folium.Polygon(locations=china_border, color='red', fill=True, fill_color='red', fill_opacity=0.3).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=1450)