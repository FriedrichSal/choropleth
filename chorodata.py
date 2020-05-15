import pandas as pd
import numpy as np
import urllib.request, json
import requests

url_wahl_2017 = 'https://opendata.duesseldorf.de/api/action/datastore/search.json?resource_id=6893a12e-3d75-4b2f-bb8b-708982bea7b7'
url_stadtteile = 'https://opendata.duesseldorf.de/sites/default/files/Stadtteile_WGS84_4326.geojson'
geo_data = requests.get(url_stadtteile).json()
data_wahl = requests.get(url_wahl_2017).json()

df_wahl = pd.DataFrame.from_dict(data_wahl['result']['records'])
sources=[{"type": "FeatureCollection", 'features': [feat]} for feat in geo_data['features']]

tx_ids=[geo_data['features'][k]['properties']['Stadtteil'] for k in range(len(geo_data['features']))]

parties = ['Wahlsieger_proz','CDU_Proz','SPD_Proz','DIE LINKE_Proz','GRÜNE_Proz','AfD_Proz','FDP_Proz']
for n in range(0,len(rate_list)):
    dct[rate_list[n]] = [df.loc[stadtteil, parties[n]] for stadtteil in tx_ids]
    dct_min[mins_list[n]] = min(dct[rate_list[n]])
    dct_max[maxs_list[n]] = max(dct[rate_list[n]])


    #Winner
pl_colorscale= [[0.0, ‘rgb(255, 255, 204)’],
[0.35, ‘rgb(161, 218, 180)’],
[0.5, ‘rgb(65, 182, 196)’],
[0.6, ‘rgb(44, 127, 184)’],
[0.7, ‘rgb(8, 104, 172)’],
[1.0, ‘rgb(37, 52, 148)’]]
#CDU
cdu_colorscale= [[0.0, ‘rgb(224, 224, 224)’],
[0.35, ‘rgb(192, 192, 192)’],
[0.5, ‘rgb(160, 160, 160)’],
[0.6, ‘rgb(128, 128, 128)’],
[0.7, ‘rgb(96, 96, 96)’],
[1.0, ‘rgb(64, 64, 64)’]]
#SPD
spd_colorscale= [[0.0, ‘rgb(255, 153, 153)’],
[0.35, ‘rgb(255, 102, 102)’],
[0.5, ‘rgb(255, 51, 51)’],
[0.6, ‘rgb(255, 0, 0)’],
[0.7, ‘rgb(204, 0, 0)’],
[1.0, ‘rgb(153, 0, 0)’]]
#Die Grünen
gruene_colorscale= [[0.0, ‘rgb(153, 255, 204)’],
[0.35, ‘rgb(102, 255, 178)’],
[0.5, ‘rgb(51, 255, 153)’],
[0.6, ‘rgb(0, 255, 128)’],
[0.7, ‘rgb(0, 204, 102)’],
[1.0, ‘rgb(0, 153, 76)’]]
#Die Linke
linke_colorscale= [[0.0, ‘rgb(255, 153, 204)’],
[0.35, ‘rgb(255, 102, 178)’],
[0.5, ‘rgb(255, 51, 153)’],
[0.6, ‘rgb(255, 0, 128)’],
[0.7, ‘rgb(204, 0, 102)’],
[1.0, ‘rgb(153, 0, 76)’]]
#AFD
afd_colorscale= [[0.0, ‘rgb(153, 255, 255)’],
[0.35, ‘rgb(102, 255, 255)’],
[0.5, ‘rgb(51, 255, 255)’],
[0.6, ‘rgb(0, 255, 255)’],
[0.7, ‘rgb(0, 204, 204)’],
[1.0, ‘rgb(0, 153, 153)’]]
#FDP
fdp_colorscale=[[0.0, ‘rgb(255, 255, 204)’],
[0.35, ‘rgb(255, 255, 153)’],
[0.5, ‘rgb(255, 255, 102)’],
[0.6, ‘rgb(255, 255, 51)’],
[0.7, ‘rgb(255, 255, 0)’],
[1.0, ‘rgb(204, 204, 0)’]]


def get_color_for_val(val, vmin, vmax, pl_colorscale):
    if vmin >= vmax:
        raise ValueError('vmin should be < vmax')
        
    plotly_scale, plotly_colors = list(map(float, np.array(pl_colorscale)[:,0])), np.array(pl_colorscale)[:,1]  
    colors_01=np.array(list(map(literal_eval,[color[3:] for color in plotly_colors] )))/255.
    
    v= (val - vmin) / float((vmax - vmin)) 

    idx = 0
   
    while(v > plotly_scale[idx+1]): 
        idx+=1
    left_scale_val = plotly_scale[idx]
    right_scale_val = plotly_scale[idx+ 1]
    vv = (v - left_scale_val) / (right_scale_val - left_scale_val)
    
    val_color01 = colors_01[idx]+vv*(colors_01[idx + 1]-colors_01[idx])
    val_color_0255 = list(map(np.uint8, 255*val_color01+0.5))
    return 'rgb'+str(tuple(val_color_0255))


facecolor_list = ['facecolor_win','facecolor_cdu','facecolor_spd','facecolor_linke','facecolor_gruene','facecolor_afd','facecolor_fdp']
scale_list = [pl_colorscale,cdu_colorscale,spd_colorscale,linke_colorscale,gruene_colorscale,afd_colorscale,fdp_colorscale]

dct_facecolor = {}
for i in facecolor_list:
    dct_facecolor['%s' % i] = None

for n in range(0,len(facecolor_list)):
    dct_facecolor[facecolor_list[n]] = [get_color_for_val(r, dct_min[mins_list[n]], dct_max[maxs_list[n]], scale_list[n]) for r in dct[rate_list[n]]] 

