from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from core.models import Movie
from .filters import MovieFilter


def index(request):
    return render(request, "homepage.html")

def format_runtime(mins):
    hours_total = mins // 60
    # Get additional minutes with modulus
    minutes_total = mins % 60
    # Create time as a string
    time_string = "{}h {}m".format(hours_total, minutes_total)
    return time_string
    
    

def index2(request):
    query = Movie.objects.all()
    movie_list = []
    
    movie_filter = MovieFilter(request.GET, queryset=Movie.objects.all())
    filtered_movies = movie_filter.qs
    if filtered_movies:
        query = filtered_movies
        
    for q in query.iterator():
        # genres_list = [x.title for x in q.genres.all().iterator()]
        movie_list.append({
            'id': q.id,
            'title': q.title,
            'rating': q.rating, 
            'runtime': format_runtime(int(q.runtime)),
            'trailer_url': q.trailer_url,
            'release_date': q.release_date,
            'pic': q.pic
        })
    # movies = query.iterator
    return render(request, "homepage2.html", {'movies': movie_list, 'movie_filter': movie_filter})