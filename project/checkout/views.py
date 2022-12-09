from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from core.models import Movie, Showing, Promo, ShowRoom, SeatInShowing, PhysicalSeat
from checkout.models import TicketFactory, Booking, TicketType
from home.views import format_runtime
import json
from .api import get_actor_info
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .adapter import login_required_message
import urllib

def get_actors(actor_ids):
    """Returns a list of tuples with actor name, actor picture"""
    #convert string list to list
    actor_ids = json.loads(actor_ids)
    actor_info = [get_actor_info(str(id)) for id in actor_ids]
    return actor_info

@login_required_message()
# @login_required (login_url='/members/login/')
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
            found = False
            for i,show in enumerate(showtimes):
                if show["datetime"].strftime("%Y %m %d") == showing.showtime.strftime("%Y %m %d"):
                    found = True
                    showtimes[i]["time"].append({'time' : showing.showtime.strftime("%H:%M:%S"), 'id': showing.id})
                    showtimes[i]["time"] = sorted(showtimes[i]["time"], key= lambda j: j['time'])
                    break
            if not found:
                showtimes.append({"datetime": showing.showtime, "day": showing.showtime.date, "time": [{'time': showing.showtime.strftime("%H:%M:%S"), 'id': showing.id}]})  

    return render(request, "select_show_time.html", {'movie': movie_info, "showtimes":showtimes})

@login_required (login_url='/members/login/')
def select_seats(request, show_id=None):
    if request.method == 'POST':
        data = request.POST
        seats = data.get("chosen_seats")
        return redirect(reverse('select_tickets_and_age', kwargs={"seats": str(seats), "show_id": show_id}))
    else:    
        if show_id:
            showing = Showing.objects.get(pk=show_id)
            #room = ShowRoom.objects.get(pk=showing.room.pk)
            showing_seats = showing.seats.all()
            seats = {}
            for i in range(len(showing_seats)):
                if showing_seats[i].physical_seat.seat_row not in seats:
                    seats[showing_seats[i].physical_seat.seat_row] = {} 
                seats[showing_seats[i].physical_seat.seat_row][showing_seats[i].physical_seat.seat_number] = showing_seats[i]    
                
        else:
            showing = None
            room = None
        return render(request, "select_seats.html", {'showing': showing, 'seats': seats.items()})


@login_required (login_url='/members/login/')
def select_tickets_and_age(request, seats, show_id):
    if request.method == 'POST':
        data = request.POST
        ad = data.get("ad")
        sr = data.get("sr")
        ch = data.get("ch")
        return redirect(reverse('order_summary', kwargs={"ad": ad, "ch": ch, "sr":sr, "seats": str(seats), "show_id": show_id}))
    else:    
        if show_id:
            showing = Showing.objects.get(pk=show_id)
        ticket_types = TicketType.objects.all()
        prices = {}
        seats = seats.split(",")
        for type in ticket_types:
            prices[type.type] = type.price    
        context = {'showing' : showing, 'seats':seats, 'prices':prices}
        return render(request, "select_tickets_and_age.html", context)


def order_summary(request, ad=None, ch=None, sr=None , seats=None, show_id=None):
    tickets = {"AD":[ad], "CH":[ch], "SR":[sr]}
    ticket_types = TicketType.objects.all()
    price = [0.00, 0.00, 0.00, 0.00]
    for type in ticket_types:
        val = type.price * tickets[type.type][0]
        tickets[type.type].append(val)
        price[0] += float(val)
    price[1] = price[0] * .08 #Sales tax percentage
    price[2] = price[0] * .1 # 10% fee for online transaction
    price[3] = price[0] + price[1] + price[2]    
    showing = Showing.objects.get(pk=show_id)
    movie = showing.movie
    seats = seats.split(",")
    phys_seats = []
    for seat in seats:
        phys_seats.append(str(SeatInShowing.objects.get(pk=int(seat)).physical_seat))
    phys_seats = ', '.join(seat for seat in phys_seats)
    #print(booking.caclculate_price())

    return render(request,"order_summary.html", {"tickets": tickets, "showing":showing, "seats": seats, "phys_seats":phys_seats, "price": price})


def checkout(request, ad=None, seats=None, show_id=None):
    tickets = {"AD" : 3, "CH" : 1, "SR": 1}
    seats = "3,6,12,18,22" #SeatInShowing
    show_id = 1
    return render(request, "checkout.html")


def confirmation(request):
    template = loader.get_template("confirmation.html")
    return HttpResponse(template.render())
