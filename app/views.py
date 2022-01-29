import osmnx as ox
import networkx as nx
import os

from django.shortcuts import render

ox.config(log_console=True, use_cache=True)

# gmaps = googlemaps.Client(key='{}'.format(os.getenv('GAPI_KEY')))

# Hardcoded values for testing
userParam = {
  "coords" : [44.2269, -76.5001],
  "distance" : 2500
}

def index(request):
  return render(request, 'index.html')



def mapper(request, userParam):
  G = ox.consolidate_intersections(ox.project_graph(ox.graph_from_point((userParam.get('coords')), dist=(userParam.get('distance') / 2), network_type='walk')), tolerance=10, rebuild_graph=True, dead_ends=False)
  gLoc = ox.distance.nearest_nodes(G, userParam.get('coords')[0], userParam.get('coords')[1])
