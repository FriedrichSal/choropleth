"""
Choropleth map example for combining plotly and flask
"""

from flask import Flask, render_template, request
import random
import json
import plotly
import os
import pandas as pd
import numpy as np
import plotly.express as px
import datetime as dt

# Init Flask app
app = Flask(__name__)
app.debug = True


# Load Landkreis map data
with open("../data/kreise.json", "r") as datafile:
    kreise = json.load(datafile)

# Load plz data
with open("../data/plz_to_kreis.json", "r") as datafile:
    plz_to_kreis = json.load(datafile)

# Reformat map data to dataframe
df_k = pd.DataFrame()
for i, feature in enumerate(kreise["features"]):
    df_k.loc[i, "id"]  = feature["id"]
    df_k.loc[i, "NAME_3"] = feature["properties"]["NAME_3"]
    df_k.loc[i, "color"] = random.random()/2


@app.route('/')
def index():
    """Render route
    """

    clicked_id = request.args.get("clicked_id")
    print(f"Clicked on kreis {clicked_id}")

    # Reset colors for all areas
    df_k.loc[df_k.color == 1, "color"] = random.random()/2

    # Mark area that was clicked
    if clicked_id is not None:
        df_k.loc[int(clicked_id), "color"] = 1

    # Build chloroplety figure with plotly
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

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    graphs = [fig]
    ids = ['graph-{}'.format(i) for i in range(len(graphs))]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # Retrieve PLZ for clicked on area
    if clicked_id is None:
        plz_data = ["n/a"]
    else:
        plz_data  = [ plz for plz, kreis_id in plz_to_kreis.items() if int(kreis_id) == int(clicked_id)]
   
    return render_template('index.html',
                           ids=ids,
                           graphJSON=graphJSON,
                           plz_data_filtered=plz_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)