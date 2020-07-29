"""Choropleth map of Duesseldorf

https://towardsdatascience.com/interactive-choropleth-maps-with-plotly-46c34fba0e48

"""


import plotly.graph_objects as go
import plotly
from plotly.offline import iplot, init_notebook_mode
import plotly.offline as off
import plotly.express as px




data = []

mapbox_access_token = 'your access token'

lons=[]
lats=[]

for k in range(len(geo_data['features'])):
    county_coords=np.array(geo_data['features'][k]['geometry']['coordinates'][0])
    m, M =county_coords[:,0].min(), county_coords[:,0].max()
    lons.append(0.5*(m+M))
    m, M =county_coords[:,1].min(), county_coords[:,1].max()
    lats.append(0.5*(m+M))
    
data = [dict(type='scattermapbox',
             lat=lats, 
             lon=lons,
             mode='markers',
             text=text_win,
             marker=dict(size=1, color='white'),
             showlegend=False,
             hoverinfo='text'`
            )] 

for a in range(1,len(text_list)):
    data.append(dict(type='scattermapbox',
                 lat=lats, 
                 lon=lons,
                 mode='markers',
                 text=text_list[a],
                 marker=dict(size=1, color='white'),
                 showlegend=False,
                 hoverinfo='text'
                ))
    
fig = go.Figure(go.Scattermapbox(
        lat=['51.2277411'],
        lon=['6.7734556'],
        mode='markers',
    ))

layers_list = ['layers1','layers2','layers3','layers4','layers5','layers6','layers7']

dct_layers = {}
for i in layers_list:
    dct_layers['%s' % i] = None
    
for l in range(0,len(layers_list)):
    dct_layers[layers_list[l]]=[dict(sourcetype = 'geojson',
             source =sources[k],
             #below="water", 
             type = 'fill',   
             color = dct_facecolor[facecolor_list[l]][k],
             opacity=0.5
            ) for k in range(len(sources))]


lay_list = [dct_layers[layers_list[0]],dct_layers[layers_list[1]],dct_layers[layers_list[2]],dct_layers[layers_list[3]],dct_layers[layers_list[4]],dct_layers[layers_list[5]],dct_layers[layers_list[6]]]


layout = dict(title='Relative Strength Of The Political Parties In Dusseldorf',
              font=dict(family='Arial Black'),
              autosize=False,
              width=1100,
              height=900,
              hovermode='closest',
              mapbox=dict(accesstoken=mapbox_access_token,
                          layers=dct_layers[layers_list[0]],
                          bearing=0,
                          center=dict(
                          lat=51.2277411, 
                          lon=6.7734556),
                          pitch=0,
                          zoom=10.5
                    ) 
              )


updatemenus = list([dict(buttons=list()), 
                    dict(direction='down',
                         showactive=True)])

party_list = ['Election Winner','CDU','SPD','DIE LINKE','Die Grünen','AfD','FDP']
vis_list = [[True,False,False,False,False,False,False],[False,True,False,False,False,False,False],[False,False,True,False,False,False,False],
           [False,False,False,True,False,False,False],[False,False,False,False,True,False,False],[False,False,False,False,False,True,False],
           [False,False,False,False,False,False,True]]


for s in range(0,len(party_list)):
    updatemenus[0]['buttons'].append(dict(args=[{'visible': vis_list[s]},
                                               {'mapbox.layers': lay_list[s]}],
                                          label=party_list[s],
                                          method='update'))

layout['updatemenus'] = updatemenus

fig = dict(data=data, layout=layout)

off.iplot({'data': data,'layout': layout}, validate=False)