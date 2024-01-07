from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Bus, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError
import time
from datetime import datetime

def render_error(request, error_message, template_name='myapp/error.html'):
    context = {'error': error_message}
    return render(request, template_name, context)

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return HttpResponseRedirect(reverse('admin:index'))
        else:
            return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')

@login_required(login_url='signin')
def findbus(request):
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r)
        
        if bus_list:
            return render(request, 'myapp/list.html', {'bus_list': bus_list, 'msg': 'Available Buses'})
        else:
            return render_error(request, "Sorry, no buses available for the selected route and date.", 'myapp/findbus.html')
    else:
        return render(request, 'myapp/findbus.html')

@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        bus = get_object_or_404(Bus, id=id_r)
        
        if bus.rem > seats_r:
            name_r = bus.bus_name
            cost = seats_r * bus.price
            source_r = bus.source
            dest_r = bus.dest
            nos_r = Decimal(bus.nos)
            price_r = bus.price
            date_r = bus.date
            time_r = bus.time
            username_r = request.user.username
            email_r = request.user.email
            userid_r = request.user.id
            rem_r = bus.rem - seats_r
            Bus.objects.filter(id=id_r).update(rem=rem_r)
            book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                       source=source_r, busid=id_r,
                                       dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                       status='BOOKED')
            print('------------book id-----------', book.id)
            return render(request, 'myapp/bookings.html', locals())
        else:
            return render_error(request, "Sorry, select fewer number of seats", 'myapp/findbus.html')
    else:
        return render(request, 'myapp/findbus.html')

@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')

        try:
            book = get_object_or_404(Book, id=id_r)
            bus = get_object_or_404(Bus, id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            Book.objects.filter(id=id_r).update(status='CANCELLED', nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            return render_error(request, "Sorry, You have not booked that bus")
    else:
        return render(request, 'myapp/findbus.html')

@login_required(login_url='signin')
def seebookings(request, new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        return render_error(request, "Sorry, no buses booked", 'myapp/findbus.html')

def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        User = get_user_model()
        try:
            user = User.objects.create_user(username=name_r, email=email_r, password=password_r)
            if user:
                login(request, user)
                return render(request, 'myapp/thank.html')
            else:
                context["error"] = "Not found, Please Sign up.."
                return render(request, 'myapp/signup.html', context)
        except:
            context["error"] = "Username already exists. Please choose a different username."
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            request.session['successful_login'] = True
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)
        else:
            context["error"] = "Not found, Please Sign up.."
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)
