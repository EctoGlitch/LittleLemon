from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import Booking
from django.contrib.auth.models import User

# for making a reservation
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        
# for login
class LoginForm(AuthenticationForm):
    pass
   
# for registration
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')









