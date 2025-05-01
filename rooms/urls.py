from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('book/', views.book_room, name='book_room'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('edit-booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin-book/', views.admin_book_room, name='admin_book_room'),



]
