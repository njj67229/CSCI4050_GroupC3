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
def select_tickets_and_age(request, seats, show_id):
    if request.method == 'POST':
        data = request.POST
        tickets = data.get("order")
        print("Tickets" + str(tickets))
        return render(request, "confirmation.html")
    else:    
        if show_id:
            showing = Showing.objects.get(pk=show_id)
        ticket_types = TicketType.objects.all()
        prices = {}
        seats = seats.split(",")
        for type in ticket_types:
            prices[type.type] = type.price    
        context = {'showing' : showing, 'seats':seats, 'prices':prices}
        print("HERE")
        return render(request, "select_tickets_and_age.html", context)


@login_required (login_url='/members/login/')
def select_seats(request, show_id=None):
    if request.method == 'POST':
        data = request.POST
        seats = data.get("chosen_seats")
        print("Seats" + str(seats))
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


def order_summary(request):
    t = TicketFactory('AD',4).get_ticket()
    t.save()
    #testing booking
    p = Promo.objects.get(pk=1) 
    booking = Booking(user=request.user, showing=t.showing, promo=p)
    booking.save()
    booking.tickets.set([t])
    booking.save()
    print(booking.caclculate_price())

    return render(request,"order_summary.html" )


def checkout(request):
    return render(request, "checkout.html")


def confirmation(request):
    template = loader.get_template("confirmation.html")
    return HttpResponse(template.render())
