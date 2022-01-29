import osmnx as ox, networkx as nx, geopandas as gpd, numpy as np
from shapely.geometry import Point
import random, math

ox.config(log_console=True, use_cache=True)

point = 44.225575, -76.501424

walkDistance = 2500
target = walkDistance / 3

G = ox.graph_from_point(point, dist=walkDistance, dist_type='network')
G = ox.project_graph(G)
G = ox.simplification.consolidate_intersections(G, tolerance=10, dead_ends=False)

point_proj, crs = ox.projection.project_geometry(Point(reversed(point)), to_crs=G.graph['crs'])

x, y = point_proj.x, point_proj.y

origin_node, routeDistance = ox.distance.nearest_nodes(G, x, y, return_dist=True)

route = [origin_node]

# while (routeDistance <= walkDistance / 2):
#   nextNode = random.choice(list(G.neighbors(origin_node)))
#   edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length') 
#   routeDistance += sum(edge_lengths)
#   print('nextNode: {}, routeDistance: {}, route: {}').format(nextNode, routeDistance, route)
#   route.append(nextNode)
#   origin_node = nextNode

# fig, ax = ox.plot_graph_route(G, route)

Route = []

def process():
  for i in G.nodes:
    route = nx.shortest_path(G, origin_node, i, weight='length')
    edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length') 
    distance = sum(edge_lengths)
    if math.isclose(distance, target, rel_tol = 100):
      Route.append(route)
      for k in G.nodes:
        route = nx.shortest_path(G, i, k, weight='length')
        edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length') 
        distance = sum(edge_lengths)
        if math.isclose(distance, target, rel_tol = 100):
          Route.append(route)
          return(Route)


process()

Route.append(nx.shortest_path(G, Route[-1][-1] , origin_node, weight='length'))

ox.plot.plot_graph_route(G, Route[0], route_colors='r', route_linewidths=4)
ox.plot.plot_graph_route(G, Route[1], route_colors='r', route_linewidths=4)
ox.plot.plot_graph_route(G, Route[2], route_colors='r', route_linewidths=4)

ox.plot.plot_graph_routes(G, Route, route_colors='r', route_linewidths=4)

















# dict.sort(key=lambda x:x[1])


# absArray = np.abs(dict - target)
# nodeAnchor = dict[absArray.argmin()]

# for i in G.nodes:
#   route = nx.shortest_path(G, nodeAnchor, i, weight='length')
#   edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length') 
#   dict.append([i, sum(edge_lengths)])

# for i in G.nodes:
#   route = nx.shortest_path(G, origin_node, i, weight='length')
#   edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length') 
#   dict2.append([i, sum(edge_lengths)])

#   # if sum(edge_lengths) <= ((walkDistance / 2) * 1.10) or sum(edge_lengths) >= ((walkDistance / 2) * 0.90):
#   #   dict.append([i, sum(edge_lengths)])