from django import forms
from .models import Booking,Room


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'date', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(available=True)