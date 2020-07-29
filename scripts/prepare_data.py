import json
import requests
from urllib.request import urlopen
import os
import pandas as pd
import plotly.express as px
import random
import shapely

# Fetch and save landkreis data
#niedrig
url_kreise = "https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/4_kreise/4_niedrig.geo.json"

# hoch 
url_kreise = "https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/4_kreise/1_sehr_hoch.geo.json"
with urlopen(url_kreise) as response:
    kreise = json.load(response)

# Save to file 
with open("data/kreise.json", "w") as outfile:
    json.dump(kreise, outfile)


# Fetch ans save PLZ data
plz_url = "https://launix.de/launix/wp-content/uploads/2019/06/PLZ.csv"
resp = requests.get(plz_url)
plzcontent = resp.content

# Save to file 
with open("data/plzdata.csv", "wb") as outfile:
    outfile.write(plzcontent)

# Alternative plz data link
# https://public.opendatasoft.com/explore/dataset/postleitzahlen-deutschland/table/

df_plz = pd.read_csv("data/plzdata.csv", delimiter=";", names=["name", "lat", "long"])

# Connect PLZ data to landkreis data
# check in which kreis the PLZ point lies
# from here https://stackoverflow.com/questions/20776205/point-in-polygon-with-geojson-in-python
from shapely.geometry import shape, Point

# check each polygon to see if it contains the point
d_plz_to_kreis = {}
plz_not_found = []
for plz, myplz in df_plz.iterrows():
    # Construct point based on lon/lat returned by geocoder
    point = Point(myplz.lat, myplz.long)
    for feature in kreise['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            print(f"Found containing polygon: {feature['id']} name: {feature['properties']['NAME_3']}")
            break
    else:
        print(f"Could not find Kreise for plz {myplz}")
        plz_not_found.append(plz)
        continue
    d_plz_to_kreis[plz] = feature["id"]

# Save for later reference
with open("data/plz_to_kreis.json", "w") as outfile:
    json.dump(d_plz_to_kreis, outfile)