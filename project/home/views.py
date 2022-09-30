<<<<<<< HEAD
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    msg = "home page"
    return HttpResponse(msg)
=======
from django.http import HttpResponse
from django.template import loader

def index(request):
  template = loader.get_template('homepage.html')
  return HttpResponse(template.render())
>>>>>>> front-end
