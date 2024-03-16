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

#FUNCTIONS###############################################################################################################
# Draw arrow for start and end point
def draw_arrow(start_point, end_point,colour):
    # Define coordinates for the line
    # start_point
    # end_point 

    # Draw a line between start and end points
    folium.PolyLine(locations=[start_point, end_point], color=colour, weight=5).add_to(m)

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
    triangle_marker = folium.RegularPolygonMarker(location=end_point, color=colour, fill_color=colour, number_of_sides=3, radius=7, rotation=bearing+30)
    triangle_marker.add_to(m)

# Swap Coordinates
def swap_coordinates(lst):
    return [lst[1], lst[0]]

title_column = st.container()
with title_column:
    st.title("MigrationMaps: An Interactive Map of Historic Migrations")

#ARROW##################################################################################################################
# Example arrow
india = [22.17261,77.912088]
pakistan = [31.559353,71.409623]
vietnam = [21.24842224, 105.77636719]
palestine = swap_coordinates([35.311307,31.963358])
chechnya = swap_coordinates([45.74626,43.281928])
ireland = swap_coordinates([-6.262132,53.35769])
usa = swap_coordinates([-77.147238,38.907229])
afghanistan = swap_coordinates([69.126882,34.640873])
serbia = swap_coordinates([20.483804,44.831246])
central_asia = swap_coordinates([62.43169,41.817029])
eastern_europe = swap_coordinates([23.944122,48.843146])
sea = swap_coordinates([115.488281,-1.406109])

# between india and pakistan
draw_arrow(india,pakistan,'blue')
draw_arrow(pakistan,india,'blue')
folium.Marker(india, popup='1947 India-Pakistan Mass Migration 10M Displaced',icon=folium.Icon(color='blue')).add_to(m)
folium.Marker(pakistan, popup='1947 India-Pakistan Mass Migration 10M Displaced',icon=folium.Icon(color='blue')).add_to(m)

# ireland to usa
draw_arrow(ireland,usa,'orange')
folium.Marker(ireland, popup='1850-1860 Irish Exodus 2M Displaced',icon=folium.Icon(color='orange')).add_to(m)
folium.Marker(usa, popup='1850-1860 Irish Exodus 2M Displaced',icon=folium.Icon(color='orange')).add_to(m)

# eastern europe to palestine
draw_arrow(eastern_europe,palestine,'green')
folium.Marker(eastern_europe, popup='1929-1939 Eastern EU to Palestine 0.25M Displaced',icon=folium.Icon(color='green')).add_to(m)
folium.Marker(palestine, popup='1929-1939 Eastern EU to Palestine 0.25M Displaced',icon=folium.Icon(color='green')).add_to(m)

# chechnya to serbia and central asia
draw_arrow(chechnya,serbia,'purple')
draw_arrow(chechnya, central_asia,'purple')
folium.Marker(chechnya, popup='1944 Chechnya to Serbia and Central Asia 0.4M Displaced',icon=folium.Icon(color='purple')).add_to(m)
folium.Marker(serbia, popup='1944 Chechnya to Serbia and Central Asia 0.4M Displaced',icon=folium.Icon(color='purple')).add_to(m)
folium.Marker(central_asia, popup='1944 Chechnya to Serbia and Central Asia 0.4M Displaced',icon=folium.Icon(color='purple')).add_to(m)

# afghanistan to pakistan
draw_arrow(afghanistan,pakistan,'red')
folium.Marker(afghanistan, popup='1850-1860 Afghani Migration 0.4M Displaced',icon=folium.Icon(color='red')).add_to(m)

# vietnam to SEA
draw_arrow(vietnam,sea,'cadetblue')
folium.Marker(vietnam, popup='1979-1987 Vietnam Exodus 1M Displaced',icon=folium.Icon(color='cadetblue')).add_to(m)
folium.Marker(sea, popup='1979-1987 Vietnam Exodus 1M Displaced',icon=folium.Icon(color='cadetblue')).add_to(m)


########################################################################################################################

# dynamically get the world-country boundaries 
res = requests.get("https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json")
df = pd.DataFrame(json.loads(res.content.decode()))
df = df.assign(id=df["features"].apply(pd.Series)["id"],
         name=df["features"].apply(pd.Series)["properties"].apply(pd.Series)["name"])

# build a dataframe of country colours scraped from wikipedia

########################################################################################################################

# a list of interesting countries - Singapore is missing!
countries = ["Ireland","United States of America","Israel","West Bank","Pakistan","Vietnam","India",
             "Romania","Poland","Hungary","Slovakia","Slovenia","Republic of Serbia","Montenegro",
             "Estonia","Czech Republic","Croatia","Bulgaria","Bosnia and Herzegovina",
             "Albania", "Ukraine", "Latvia", "Lithuania", "Belarus","Moldova",
             "Kazakstan", "Kyrgyzstan", "Uzbekistan", "Tajikistan", "Turkmenistan", "Afghanistan",
             "Brunei", "Burma", "Cambodia", "Indonesia", "Laos", "Malaysia", "Philippines", "Singapore", "Thailand"]

# overlay desired countries over folium map
for r in df.loc[df["name"].isin(countries)].to_dict(orient="records"):
    folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"]).add_to(m)

########################################################################################################################
# call to render Folium map in Streamlit
st_data = st_folium(m, width=1450)