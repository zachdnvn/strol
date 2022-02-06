# strol.
<p align="center">strol. is an online web tool that generates 'strols' - cyclic paths that are of a desired length. The tool's main purpose is to incentivize going outside by diversifying the path that you would take on a frequent walk which in turn makes every journey unique.</p>

# Preview
<p align="center"><img src="https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/001/812/212/datas/original.jpg"></p>
<p align="center"><img src="https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/001/812/513/datas/gallery.jpg">
<img src="https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/001/812/514/datas/gallery.jpg">
<img src="https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/001/815/859/datas/gallery.jpg"></p>




## Inspiration
The pandemic has drastically impacted us in a number of ways, but the biggest change is definitely the alienation that many of us are facing being stuck inside. A study analyzing the effects of the stay-home order that was conducted on over 3,500 people showed that over 60% experienced depression, and about 53% experienced sleep disturbance. There is very clearly an issue with the current landscape, and as there is no foreseeable end to this ‘new normal’, we need to remain proactive during the pandemic to counteract this.

## How it Works
- The user enters their location using the textbox
  - Google’s Geocoding API returns a set of locations from the user
    - If there are multiple location returns, we can analyze the HTTP headers to best determine the proper location.
    - We then parse the returned JSON to extract the geographical coordinates.
- Next, the street network is generated around the user's location with the distance that the user inputted - serving as the bounds for the map.
  - The map is projected to allow us to preform operations on the network.
  - The network is simplified to remove non-walkable paths like highways and dead-end streets, and the finished network is cached on the server to speed up future operations.  
- Next, the the nearest node to the start location is determined
  - A node serves as a waypoint for the path generation and consists of intersections, start of paths, landmarks etc.
  - The users start location is projected onto the map to find the nearest node
  - In our tests, the nearest node is typically within 100m of the start location
  - The route between the start location and the start node is recorded and plotted.
- Next, Breadth-First traversal is performed on the network, in which we extract the node that would serve as the farthest point in the strol
  - This node is randomly selected from a set of candidates - helping randomize the path for each new strol.
- The next node is found by performing a Depth-First Traversal on that anchor node randomly selecting a nearby node.
  - This process is biased to make sure that the user isn’t being routed farther from the anchor.
Dijkstra’s algorithm is performed on that the node back to the starting location, in which a set of return paths are generated
  - A return path is randomly selected and plotted


## Technologies Used
- Google Cloud
- Docker
- Django
- Bootstrap
- NetworkX
- Google Maps API
- PROJ


