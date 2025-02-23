from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from rest_framework import generics, status, viewsets
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Menu, Booking
from .forms import BookingForm, LoginForm, SignUpForm
from django.contrib.auth.models import User
from .serializers import MenuSerializer, BookingSerializer, UserSerializer, LoginSerializer
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, csrf_protect
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import  login, logout
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import parser_classes, api_view, permission_classes
from rest_framework.authtoken.models import Token
import json
from django.contrib.auth.forms import AuthenticationForm
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.sessions.models import Session
import datetime
from django.views import View
import logging
from rest_framework_simplejwt.tokens import AccessToken
# Create your views here.
logger = logging.getLogger(__name__)

def print_test():
    data = 'error in data'
    print(data)

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

# 
@method_decorator(csrf_exempt, name='dispatch')
@permission_classes([AllowAny])
class APILoginView(APIView):
    @csrf_exempt
    def post(self, request):
        print("POST request received")
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                # _ bool for token obj
                print()
                print("Token created: ", token)
                return Response({"Response": "login sucessful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class BLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        print("BLoginView called")
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})   

class APISignUpView(APIView):
    def post(self, request):
        form = SignUpForm(request.data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print("User created: ", user)
            print("Token created: ", token)
            return Response({"Response": "signup sucessful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BSignUpView(View):
    def get(self, request):
        form = SignUpForm()
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        print("BSignUpView called")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form, 'error': 'Invalid credentials'})


@api_view(['GET', 'POST'])
@permission_classes([])
def logoutView(request):
    if request.method == "GET":
        # Handle session-based logout
        try:
            logout(request)
            return redirect('home')
        except Exception as e:
            print(f"Error during session logout: {e}")
            return Response({"error": str(e)}, status=500)

    elif request.method == "POST":
        # Handle token-based logout
        try:
            if 'HTTP_AUTHORIZATION' in request.headers and request.headers['HTTP_AUTHORIZATION'].startswith('Token'):
                user = request.user  # Token authentication is used
                logout(request)
                request.session.flush()
                request.session.cycle_key()
                return redirect('home')
            else:
                print("No valid token found for logout")
                return Response({"error": "Invalid authentication method"}, status=401)
        except Exception as e:
            print(f"Error during token-based logout: {e}")
            return Response({"error": str(e)}, status=500)



@method_decorator(csrf_exempt, name='dispatch')
@parser_classes([JSONParser, MultiPartParser, FormParser])
class BookView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            date = request.GET.get('date')
            bookings = Booking.objects.filter(booking_date=date)
            data = []
            for booking in bookings:
                data.append({
                    'fields': {
                        'name': booking.name,
                        'no_of_guests': booking.no_of_guests,
                        'time_slot': booking.time_slot,
                        'booking_date': booking.booking_date
                    }
                })
            return JsonResponse(data, safe=False)
        else:
            form = BookingForm()
            return render(request, 'book.html', {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            # print("Received data:", request.data)

            # Determine the type of data received
            if 'name' in request.data and 'no_of_guests' in request.data and 'time_slot' in request.data and 'booking_date' in request.data:
                serializer = BookingSerializer(data=request.data)
                if serializer.is_valid():
                    booking = serializer.save()
                    return JsonResponse(serializer.data, status=201)

            # If no specific fields are found, assume JSON data
            elif isinstance(request.data, dict):
                serializer = BookingSerializer(data=request.data)
                if serializer.is_valid():
                    booking = serializer.save()
                    # print("Booking created:", booking)
                    return JsonResponse(serializer.data, status=201)

            # Return validation errors or indicate invalid request
            # print("Validation errors:", serializer.errors if 'is_valid' in locals() and not serializer.is_valid() else "No valid data found")
            return Response({"error": "Invalid or missing fields"}, status=400)

        except Exception as e:
            # print("Unexpected error:", str(e))
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)


class MenuView(generics.ListCreateAPIView, TemplateView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu.html'

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Handle AJAX request
            queryset = Menu.objects.all()
            serializer = MenuSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            # Handle normal template request
            context = {
                'menu_items': Menu.objects.all()  # Match template variable name
            }
            return render(request, self.template_name, context)


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


#api views
class UserViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer
   permission_classes = [permissions.IsAuthenticated]


class MenuItemView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    serializer_class = MenuSerializer





#testing
# testing csrf token
class CsrfTestView(View):
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        print(request)
        print(request.META.get('CSRF_COOKIE'))
        return HttpResponse("CSRF token validated!")

    def post(self, request):
        print(request) #debugging
        return HttpResponse("CSRF token validated!")