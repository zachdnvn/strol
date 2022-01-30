import googlemaps
import os
import osmnx as ox, networkx as nx, geopandas as gpd, numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon
import random, math
from django.shortcuts import render
from .forms import locForm

gmaps = googlemaps.Client(key='{}'.format(os.getenv('GAPI_KEY')))

ox.config(log_console=True, use_cache=True)

walkDistance = 2500
target = walkDistance / 2

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
  G = ox.project_graph(G)
  G = ox.simplification.consolidate_intersections(G, tolerance=10, dead_ends=False)

  point_proj, crs = ox.projection.project_geometry(Point(reversed(point)), to_crs=G.graph['crs'])

  x, y = point_proj.x, point_proj.y

  origin_node, routeDistance = ox.distance.nearest_nodes(G, x, y, return_dist=True)

  route = [origin_node]

  Route = []

  dict = []
  distance = 0
  for i in G.nodes:
    route = nx.shortest_path(G, origin_node, i, weight='length')
    edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length') 
    distance = sum(edge_lengths)
    if math.isclose(distance, target, abs_tol = 250):
      dict.append([i, sum(edge_lengths)])

  anchorNode = random.choice(dict)
  Route.append(nx.shortest_path(G, origin_node, anchorNode[0], weight='length'))
  Route.append(nx.shortest_path(G, Route[0][-1], random.choice(list(nx.descendants_at_distance(G, Route[0][-1], 3))), weight='length'))
  Route.append(nx.shortest_path(G, Route[1][-1], origin_node, weight='length'))

  distance = sum(ox.utils_graph.get_route_edge_attributes(G, Route[0], 'length'))
  distance += sum(ox.utils_graph.get_route_edge_attributes(G, Route[1], 'length'))
  distance += sum(ox.utils_graph.get_route_edge_attributes(G, Route[2], 'length'))

  print('Distance is {} m.'.format(distance))

  fig, ax = ox.plot.plot_graph_routes(G, Route, route_colors='r', route_linewidths=4,save=True)

