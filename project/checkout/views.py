from django.http import HttpResponse
from django.template import loader

def select_show_time(request):
  template = loader.get_template('select_show_time.html')
  return HttpResponse(template.render())

def confirmation(request):
  template = loader.get_template('confirmation.html')
  return HttpResponse(template.render())