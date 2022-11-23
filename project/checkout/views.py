from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from core.models import Movie, Showing
from home.views import format_runtime
import json
from .api import get_actor_info
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
            print(showing.id)
            found = False
            for i,show in enumerate(showtimes):
                if show["datetime"].strftime("%Y %m %d") == showing.showtime.strftime("%Y %m %d"):
                    found = True
                    showtimes[i]["time"].append(showing.showtime.strftime("%H:%M:%S"))
                    showtimes[i]["time"].sort()        
                    break
            if not found:
                showtimes.append({"datetime": showing.showtime, "day": showing.showtime.date, "time": [showing.showtime.strftime("%H:%M:%S")]})  
    
    print(showtimes)
    
    return render(request, "select_show_time.html", {'movie': movie_info, "showtimes":showtimes})

@login_required (login_url='/members/login/')
def select_tickets_and_age(request):
    template = loader.get_template("select_tickets_and_age.html")
    return HttpResponse(template.render())


@login_required (login_url='/members/login/')
def select_seats(request, show_id=None):
    if show_id:
        showing = Showing.objects.get(pk=show_id)
        print(showing)
    else:
        showing = None
    return render(request, "select_seats.html", {'showing': showing})


def order_summary(request):
    template = loader.get_template("order_summary.html")
    return HttpResponse(template.render())


def checkout(request):
    return render(request, "checkout.html")


def confirmation(request):
    template = loader.get_template("confirmation.html")
    return HttpResponse(template.render())
