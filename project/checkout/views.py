from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from core.models import Movie, Showing, Promo, ShowRoom, SeatInShowing, PhysicalSeat
from checkout.models import TicketFactory, Booking, TicketType, Ticket
from home.views import format_runtime
import json
from .api import get_actor_info
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .adapter import login_required_message
from django.core.mail import send_mail
from accounts.models import PaymentCard

from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template

from django.views.generic.list import ListView



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
def select_tickets_and_age(request, seats=None, show_id=None):
    if show_id:
            showing = Showing.objects.get(pk=show_id)
    return render(request, "select_tickets_and_age.html", {'showing': showing, 'seats': seats})


@login_required (login_url='/members/login/')
def select_seats(request, show_id=None):
    if request.method == 'POST':
        data = request.POST
        seats = data.get("chosen_seats")
        return select_tickets_and_age(request, seats, show_id)
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


def order_summary(request, tickets=None, seats=None, show_id=None):
    tickets = {"AD" : 3, "CH" : 1, "SR": 1}
    seats = "3,6,12,18,22" #SeatInShowing
    show_id = 1
    
    #t = TicketFactory('AD',1).get_ticket()
    #t.save()
    #testing booking
    #p = Promo.objects.get(pk=1) 
    #booking = Booking(user=request.user, showing=t.showing)
    #booking.save()
    #booking.tickets.set([t])
    #booking.save()
    #print(booking.caclculate_price())

    return render(request,"order_summary.html" )


def checkout(request, tickets=None, seats=None, show_id=None):
    tickets = {"AD" : 3, "CH" : 1, "SR": 1}
    seats = "3,6,12,18,22" #SeatInShowing
    show_id = 1
    email = 'yalini.nadar@gmail.com'
    promo = None
            
    def calculate_total(promo=None):
        """calculates total ticket prices"""
        total = 0
        for key in tickets:
            t_t = TicketType.objects.filter(type = key).first()
            total += t_t.price * tickets[key]
        if promo:
            total = total * (1-promo)
        return total
        
        # print(TicketType.objects.all())
    def send_email():
        """sends email confirmation to given email"""
        email = 'yalini.nadar@gmail.com'
        
        message = get_template("email.html").render()

        email = EmailMessage(
            subject='Hello',
            body=message,
            from_email='teamc3movies@gmail.com',
            to=['yalini.nadar@gmail.com'],
            headers={'Message-ID': 'foo'},
        )
        email.content_subtype = "html"
        email.send()
    
    total = calculate_total()
    # send_email()
    if request.method == 'POST':
        promo_code = request.POST['promo_code']
        promo = Promo.objects.filter(code = promo_code).first()
        
        #Apply Promo
        if not promo:
            messages.error(request,'Promo Code Does Not Exist')
            promo = None
        # print(promo.exp_date)
        elif (promo.exp_date >= datetime.now().date()):
            messages.error(request, 'Sorry this promo is expired')
            promo = None
        else:
            print('yay')
            messages.success(request,'Promo Code has been added!')
            promo = promo
    
    #create multiple ticket objects and saves them to the db
    tickets_cleaned = []
    for key in tickets:
        for idx in range(tickets[key]):
            tickets_cleaned.append(key)
    
    ticket_ids = []
    for item in tickets_cleaned:
        t = TicketFactory(item,show_id).get_ticket()
        t.save()
        ticket_ids.append(t.pk)
        
    print(ticket_ids)
      
    #create booking object
    s = Showing.objects.filter(pk = show_id).first()
    booking = Booking(user=request.user, showing=s, promo=promo)
    booking.save()
    for id in ticket_ids:
        booking.tickets.add(id)
        booking.save()
    print(booking)
    
    # print(our_tickets)
        
    curr_cards = PaymentCard.objects.filter(card_owner=request.user).all()

    return render(request, "checkout.html", {'card':curr_cards, 'total': total})


def confirmation(request):
    b = Booking.objects.filter(user=request.user).first()
    print(b.tickets.all())
    return render(request,"confirmation.html")

def order_history(request):
    orders = Booking.objects.filter(user=request.user)
    final = []
    #need to organize tickets
        
    for item in orders:
        res = {
            'booking_id' : item.pk,
            'showing': item.showing,
            'tix': item.tickets.all()
        }
        final.append(res)
    
    print(final)
        
    print(orders)
    return render(request, "order_history.html", {'order': final} )
