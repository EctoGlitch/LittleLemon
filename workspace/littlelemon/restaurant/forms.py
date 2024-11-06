from django.forms import ModelForm
from .models import Booking

# for making a reservation
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"