from django.http import HttpResponse
from django.template import loader

def register(request):
  template = loader.get_template('register.html')
  return HttpResponse(template.render())

def account_confirmation(request):
  template = loader.get_template('account_confirmation.html')
  return HttpResponse(template.render())  

def login(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render())