"""
Example for combining plotly and flask

Returns:
    [type]: [description]
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
app = Flask(__name__)
app.debug = True


# load data
with open("../data/kreise.json", "r") as datafile:
    kreise = json.load(datafile)

with open("../data/plz_to_kreis.json", "r") as datafile:
    plz_to_kreis = json.load(datafile)

df_k = pd.DataFrame()
for i, feature in enumerate(kreise["features"]):
    df_k.loc[i, "id"]  = feature["id"]
    df_k.loc[i, "NAME_3"] = feature["properties"]["NAME_3"]
    df_k.loc[i, "color"] = random.random()/2



@app.route('/')
def index():

    clicked_id = request.args.get("clicked_id")
    print(f"Clicked on kreis {clicked_id}")

    # Reseld color for unclicked map
    df_k.loc[df_k.color == 1, "color"] = random.random()/2

    if clicked_id is not None:
        df_k.loc[int(clicked_id), "color"] = 1

    print(f"1 ======= {dt.datetime.now() }")
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

    # fig.show()

    graphs = [fig]
    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i in range(len(graphs))]

    print(f"2 ======= {dt.datetime.now() }")

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    print(f"3 ======= {dt.datetime.now() }")

    if clicked_id is None:
        plz_data = ["n/a"]
    else:
        plz_data  = [ plz for plz, kreis_id in plz_to_kreis.items() if int(kreis_id) == int(clicked_id)]
        # plz_data = list(plz_to_kreis.keys())
    print(plz_data)

    print(f"4 ======= {dt.datetime.now() }")


    # import pdb; pdb.set_trace()

    return render_template('index.html',
                           ids=ids,
                           graphJSON=graphJSON,
                           plz_data_filtered=plz_data)
                        #    plz_to_kreis=json.dumps(plz_to_kreis))



    # return render_template('index.html',
    #                        ids=ids,
    #                        graphJSON=graphJSON)



# @app.route('/old')
# def index_old():
#     rng = pd.date_range('1/1/2011', periods=7500, freq='H')
#     ts = pd.Series(np.random.randn(len(rng)), index=rng)

#     graphs = [
#         dict(
#             data=[
#                 dict(
#                     x=[1, 2, 3],
#                     y=[10, 20, 30],
#                     type='scatter'
#                 ),
#             ],
#             layout=dict(
#                 title='first graph'
#             )
#         ),

#         dict(
#             data=[
#                 dict(
#                     x=[1, 3, 5],
#                     y=[10, 50, 30],
#                     type='bar'
#                 ),
#             ],
#             layout=dict(
#                 title='second graph'
#             )
#         ),

#         dict(
#             data=[
#                 dict(
#                     x=ts.index,  # Can use the pandas data structures directly
#                     y=ts
#                 )
#             ]
#         )
#     ]

#     # Add "ids" to each of the graphs to pass up to the client
#     # for templating
#     ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

#     # Convert the figures to JSON
#     # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
#     # objects to their JSON equivalents
#     graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # plz_data = list(plz_to_kreis.keys())[:20]
    # print(plz_data)

    # return render_template('index.html',
    #                        ids=ids,
    #                        graphJSON=graphJSON,
    #                        plz_data=plz_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)