from django.shortcuts import render

def index(request):
  return render(request, 'index.html')

def app(request):
  return render(request, 'app/index.html')