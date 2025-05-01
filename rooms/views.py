from django.shortcuts import render
from .models import Room
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BookingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Booking

# get all rooms from db and pass them to room list
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


@login_required
def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('room_list')  # go back to rooms page
    else:
        form = BookingForm()

    return render(request, 'rooms/book_room.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in after signup
            return redirect('room_list')
    else:
        form = UserCreationForm()
    return render(request, 'rooms/register.html', {'form': form})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'rooms/my_bookings.html', {'bookings': bookings})
