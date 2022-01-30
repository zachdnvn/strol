import googlemaps
import os
import osmnx as ox, networkx as nx, geopandas as gpd, numpy as np, plotly.express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon
import random, math
from django.shortcuts import render
from .forms import locForm
from IPython.display import IFrame
from django.shortcuts import redirect

gmaps = googlemaps.Client(key='{}'.format(os.getenv('GAPI_KEY')))
px.set_mapbox_access_token('{}'.format(os.getenv('MB_KEY')))

ox.config(log_console=True, use_cache=True)

walkDistance = 2500
target = walkDistance / 2
genMap = 1

# Hardcoded values for testing
points = (44.2269, -76.5001)
def index(request):
  return render(request, 'index.html')

def app(request):
  if request.method == 'POST':
    form = locForm(request.POST)
    if form.is_valid():
      cleaned_info = form.cleaned_data
      mapper(request, cleaned_info)
  else:
    form = locForm()
  return render(request, 'app.html', {'form':form})

def mapper(request, info):
  geocode_result = gmaps.geocode(info['Location'])
  point = (geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng'])


  G = ox.graph_from_point(point, dist=walkDistance, dist_type='network')
  # G = ox.project_graph(G)
  # G = ox.simplification.consolidate_intersections(G, tolerance=10, dead_ends=False)

  # point_proj, crs = ox.projection.project_geometry(Point(reversed(point)), to_crs=G.graph['crs'])

  # x, y = point_proj.x, point_proj.y

  origin_node, routeDistance = ox.distance.nearest_nodes(G, point[0], point[1], return_dist=True)

  Route = []

  dict = []
  distance = 0
  for i in G.nodes:
    route = nx.shortest_path(G, origin_node, i, weight='length')
    edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length') 
    distance = sum(edge_lengths)
    if math.isclose(distance, target, abs_tol = 100):
      dict.append([i, sum(edge_lengths)])

  anchorNode = random.choice(dict)
  Route1 = nx.shortest_path(G, origin_node, anchorNode[0], weight='length')
  Route2 = nx.shortest_path(G, Route1[-1], random.choice(list(nx.descendants_at_distance(G, Route1[-1], 3))), weight='length')
  Route3 = nx.shortest_path(G, Route2[-1], origin_node, weight='length')

  # distance = sum(ox.utils_graph.get_route_edge_attributes(G, Route1, 'length'))
  # distance += sum(ox.utils_graph.get_route_edge_attributes(G, Route2, 'length'))
  # distance += sum(ox.utils_graph.get_route_edge_attributes(G, Route3, 'length'))

  print('Distance is {} m.'.format(distance))

  # nodes = ox.graph_to_gdfs(G, edges=False)

  # lonn = []
  # latt = []

  # for c, i in enumerate(Route[0]):
  #   # if (nodes['lon'][Route[0][c]] != 'nan' and nodes['lat'][Route[0][c]] != 'nan'):
  #   #   lonn.append(nodes['lon'][Route[0][c]])
  #   #   latt.append(nodes['lat'][Route[0][c]])
  #   pointt = G.nodes[c]
  #   lonn.append(pointt['x'])
  #   latt.append(pointt['y'])
  
  # print(lonn)
  # print(latt)

  # fig = go.Figure(go.Scattermapbox(
  #   mode = "lines+markers",
  #   lon = lonn,
  #   lat = latt,
  #   marker = {'size': 10},
  # ))

  

  # fig.update_layout(mapbox_style="stamen-terrain",
  #     mapbox_center_lat = point[0], mapbox_center_lon=point[1])
  # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
  #                   mapbox = {
  #                       'center': {'lat': point[0], 
  #                       'lon': point[1]},
  #                       'zoom': 13})

  # fig.show()
  # mpl_fig = plt.figure()
  # plot = ox.plot_graph_routes(G, Route, route_colors='r', show=False)

  # fit.show()

  # m2 = ox.plot_route_folium(G, Route[0], weight=10)
  # filepath = "app/templates/app/route.html"
  # # m2.save(filepath)
  # print(Route[0])
  # print(Route[1])
  # print(Route[2])

  # m1 = ox.plot_graph_folium(G, popup_attribute="name", weight=2, color="#8b0000")
  # filepath = "app/templates/app/graph.html"
  # m1.save(filepath)
  # IFrame(filepath, width=600, height=500)

  m1 = ox.plot_route_folium(G, Route1, popup_attribute="length")
  m2 = ox.plot_route_folium(G, Route2, route_map = m1, popup_attribute="length")
  m3 = ox.plot_route_folium(G, Route3, route_map = m2, popup_attribute="length")


  
  
  
  filepath = "app/templates/app/route.html"
  # m31.save('m31.html')
  # m32.save('m32.html')
  m3.save(filepath)
  # # IFrame(filepath, width=600, height=500)

  # # route_map = ox.plot_route_folium(G, Route[0], route_color='#ff0000', opacity=0.5)
  # # route_map.save('route.html')

  return redirect('route.html')