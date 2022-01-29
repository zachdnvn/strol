import osmnx as ox, networkx as nx, geopandas as gpd
from shapely.geometry import Point
import random

ox.config(log_console=True, use_cache=True)

point = 44.225575, -76.501424

walkDistance = 2500

G = ox.graph_from_point(point, dist=walkDistance, dist_type='network')
G = ox.project_graph(G)
G = ox.simplification.consolidate_intersections(G, tolerance=10, dead_ends=False)

point_proj, crs = ox.projection.project_geometry(Point(reversed(point)), to_crs=G.graph['crs'])

x, y = point_proj.x, point_proj.y

origin_node, routeDistance = ox.distance.nearest_nodes(G, x, y, return_dist=True)

route = [origin_node]

while (routeDistance <= walkDistance / 2):
  nextNode = random.choice(list(G.neighbors(origin_node)))
  edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length') 
  routeDistance += sum(edge_lengths)
  print('nextNode: {}, routeDistance: {}, route: {}').format(nextNode, routeDistance, route)
  route.append(nextNode)
  origin_node = nextNode

fig, ax = ox.plot_graph_route(G, route)