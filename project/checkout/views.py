from django.http import HttpResponse
from django.template import loader

def select_show_time(request):
  template = loader.get_template('select_show_time.html')
  return HttpResponse(template.render())

def select_tickets_and_age(request):
  template = loader.get_template('select_tickets_and_age.html')
  return HttpResponse(template.render())

def select_seats(request):
  template = loader.get_template('select_seats.html')
  return HttpResponse(template.render())

def order_summary(request):
  template = loader.get_template('order_summary.html')
  return HttpResponse(template.render())

def checkout(request):
  template = loader.get_template('checkout.html')
  return HttpResponse(template.render())

def confirmation(request):
  template = loader.get_template('confirmation.html')
  return HttpResponse(template.render())