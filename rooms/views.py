from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Room, Booking
from .forms import BookingForm

# get all rooms from db and pass them to room list
def room_list(request):
    show_available = request.GET.get('available') == '1'

    if show_available:
        rooms = Room.objects.filter(available=True)
    else:
        rooms = Room.objects.all()

    return render(request, 'rooms/room_list.html', {
        'rooms': rooms,
        'show_available': show_available
    })


@login_required
def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if not booking.room.available:
                messages.error(request, "That room is currently unavailable.")
                return redirect('book_room')
            booking.user = request.user
            booking.save()
            messages.success(
                request,
                f"Booking confirmed for {booking.room.name} on {booking.date} at {booking.start_time}."
            )
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
            messages.success(request, "Account created successfully! Welcome.")
            return redirect('room_list')
    else:
        form = UserCreationForm()
    return render(request, 'rooms/register.html', {'form': form})

@login_required
def my_bookings(request):
    query = request.GET.get('q', '')
    bookings = Booking.objects.filter(user=request.user)

    if query:
        bookings = bookings.filter(
            room__name__icontains=query
        )

    return render(request, 'rooms/my_bookings.html', {
        'bookings': bookings,
        'query': query
    })

# ensure user can only change their bookings
@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        messages.info(request, "Booking updated successfully.")
        return redirect('my_bookings')
    return render(request, 'rooms/edit_booking.html', {'form': form})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.error(request, "Booking cancelled.")
        return redirect('my_bookings')
    return render(request, 'rooms/confirm_cancel.html', {'booking': booking})

@staff_member_required
def admin_book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        user_id = request.POST.get('user')
        if form.is_valid() and user_id:
            booking = form.save(commit=False)
            booking.user = User.objects.get(id=user_id)
            booking.save()
            messages.success(request, f"Booking made on behalf of {booking.user.username}.")
            return redirect('room_list')
    else:
        form = BookingForm()
        users = User.objects.all()
    return render(request, 'rooms/admin_book.html', {'form': form, 'users': users})
