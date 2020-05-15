import json
from urllib.request import urlopen

import pandas as pd
import plotly.express as px
import random

# https://github.com/SBejga/germany-administrative-geojson
# https://github.com/isellsoap/deutschlandGeoJSON
# https://public.opendatasoft.com/explore/dataset/landkreise-in-germany/export/

# plz data
# https://public.opendatasoft.com/explore/dataset/postleitzahlen-deutschland/table/
# https://launix.de/launix/launix-gibt-plz-datenbank-frei/
#

# point in landkreise
# https://stackoverflow.com/questions/20776205/point-in-polygon-with-geojson-in-python
"""
https://plotly.com/python/choropleth-maps/
This can either be a supplied GeoJSON file where each feature has either an id field or some identifying value in properties
"""

# States
states = json.loads("states.json")

mydf = pd.DataFrame()
for feature in states["features"]:
    fid = feature["id"]
    name = feature["properties"]["name"]
    mydf.loc[int(fid), "id"] = fid
    mydf.loc[int(fid), "name"] = name
    mydf.loc[int(fid), "color"] = random.random()


# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
#                    dtype={"fips": str})


fig = px.choropleth(
    mydf,
    geojson=states,
    locations="id",
    color="color",
    color_continuous_scale="Viridis",
    range_color=(0, 1),
    scope="europe",
    labels={"name": "name"},
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(geo={"showcountries": False, "showcoastlines": False})
# fig.update_layout(scale=2)
fig.update_geos(fitbounds="locations", visible=False)

fig.show()

# no map

import plotly.express as px

df = px.data.election()
geojson = px.data.election_geojson()

fig = px.choropleth(
    df,
    geojson=geojson,
    color="Bergeron",
    locations="district",
    featureidkey="properties.district",
    projection="mercator",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()



# Landkreise
url_landkrise = "https://public.opendatasoft.com/explore/dataset/landkreise-in-germany/download/?format=geojson&timezone=Europe/Berlin&lang=en"
with urlopen(url_landkrise) as response:
    landkreise = json.load(response)


df_lk = pd.DataFrame()
for i, feature in enumerate(landkreise["features"]):
    name = feature["properties"]["name_2"]
    df_lk.loc[i, "name_2"] = name
    df_lk.loc[i, "color"] = random.random()
    df_lk.loc[i, "hasc_2"] = feature["properties"]["hasc_2"]

fig = px.choropleth(
    df_lk,
    geojson=landkreise,
    locations="hasc_2",
    color="color",
    featureidkey="properties.hasc_2",
    color_continuous_scale="Viridis",
    range_color=(0, 1),
    labels={"name_2": "name_2"},
    projection="mercator"
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_geos(fitbounds="locations", visible=False)

fig.show()


# Kreise



#niedrig
url_kreise = "https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/4_kreise/4_niedrig.geo.json"

# hoch 
url_kreise = "https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/4_kreise/1_sehr_hoch.geo.json"
with urlopen(url_kreise) as response:
    kreise = json.load(response)

# Save to file 
with open("data/kreise.json"), "w") as outfile:
    json.dump(data, outfile)


df_k = pd.DataFrame()
for i, feature in enumerate(kreise["features"]):
    df_k.loc[i, "id"]  = feature["id"]
    df_k.loc[i, "NAME_3"] = feature["properties"]["NAME_3"]
    df_k.loc[i, "color"] = random.random()

fig = px.choropleth(
    df_k,
    geojson=kreise,
    locations="id",
    color="color",
    # featureidkey="properties.hasc_2",
    color_continuous_scale="Viridis",
    range_color=(0, 1),
    labels={"NAME_3": "NAME_3"},
    projection="mercator"
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_geos(fitbounds="locations", visible=False)

fig.show()
