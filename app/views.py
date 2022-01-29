import osmnx as ox
import networkx as nx
import googlemaps
import os

from django.shortcuts import render
from .forms import locForm

gmaps = googlemaps.Client(key='{}'.format(os.getenv('GAPI_KEY')))

ox.config(log_console=True, use_cache=True)

# Hardcoded values for testing
userParam = {
  "coords" : [44.2269, -76.5001],
  "distance" : 2500
}

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
 coords = (geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['long'])
  # return render(request, 'app.html',{})

