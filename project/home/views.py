from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from core.models import Movie, Showing
from .filters import MovieFilter


def index(request):
    return render(request, "homepage2.html")

def format_runtime(mins):
    hours_total = mins // 60
    # Get additional minutes with modulus
    minutes_total = mins % 60
    # Create time as a string
    time_string = "{}h {}m".format(hours_total, minutes_total)
    return time_string
    
    

def index2(request, showing_type=None):
    query = Movie.objects.all()
    if showing_type=='coming_soon':
        #need to show coming soon movies
        # showings = Showing.objects.all()
        query = query.filter(showing__isnull=True)
    elif showing_type=='now_showing':
        query = query.filter(showing__isnull=False).distinct()
        
    message = ""
    movie_list = []
    
    movie_filter = MovieFilter(request.GET, queryset=query)
    filtered_movies = movie_filter.qs
    if filtered_movies:
        query = filtered_movies
    else:
        #no results from query
        message = 'Could not find any movies matching that query. Please try again...'
        
    for q in query.iterator():
        genres_list = [x.title for x in q.genres.all().iterator()]
        movie_list.append({
            'id': q.id,
            'title': q.title,
            'rating': q.rating, 
            'runtime': format_runtime(int(q.runtime)),
            'trailer_url': q.trailer_url,
            'release_date': q.release_date,
            'pic': q.pic,
            'genres': genres_list
        })
    # movies = query.iterator
    return render(request, "homepage2.html", {'movies': movie_list, 'movie_filter': movie_filter, 'msg': message})