from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from core.models import Movie, Showing
from home.views import format_runtime
import json
from .api import get_actor_info

def get_actors(actor_ids):
    """Returns a list of tuples with actor name, actor picture"""
    #convert string list to list
    actor_ids = json.loads(actor_ids)
    actor_info = [get_actor_info(str(id)) for id in actor_ids]
    return actor_info

def select_show_time(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    genres_list = [x.title for x in movie.genres.all().iterator()]
    actor_info = [(x.name, x.pic) for x in movie.actor_ids.all().iterator()]
    # actor_info = get_actors(movie.actor_ids)
    if movie.producer is None:
        producer = 'N/a'
    else:
        producer = movie.producer
    movie_info = {
            'id': movie_id,
            'title': movie.title,
            'tag': movie.tag,
            'rating': movie.rating, 
            'runtime': format_runtime(int(movie.runtime)),
            'release_date': movie.release_date,
            'synopsis': movie.synopsis,
            'pic': movie.pic,
            'trailer_url': movie.trailer_url,
            'producer': producer,
            'director': movie.director,
            'genres': genres_list,
            'actors': actor_info,
    }
    showings = Showing.objects.filter(movie__pk=movie_id)
    showtimes = []
    for showing in showings:
        showtimes.append({"day": showing.showtime.date, "time": showing.showtime.time})
    return render(request, "select_show_time.html", {'movie': movie_info, "showtimes":showtimes})


def select_tickets_and_age(request):
    template = loader.get_template("select_tickets_and_age.html")
    return HttpResponse(template.render())


def select_seats(request):
    template = loader.get_template("select_seats.html")
    return HttpResponse(template.render())


def order_summary(request):
    template = loader.get_template("order_summary.html")
    return HttpResponse(template.render())


def checkout(request):
    return render(request, "checkout.html")


def confirmation(request):
    template = loader.get_template("confirmation.html")
    return HttpResponse(template.render())
