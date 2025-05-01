from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('book/', views.book_room, name='book_room'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

]
