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

class APIBookview(generics.GenericAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def list(self, request, *args, **kwargs):
        date = request.GET.get('date')
        data = []
        if date:
            for booking in Booking.objects.filter(booking_date=date):
                data.append({
                    'name': booking.name,
                    'no_of_guests': booking.no_of_guests,
                    'time_slot': booking.time_slot,
                    'booking_date': booking.booking_date
                    })
            if len(data) == 0:
                 return JsonResponse({'response': 'No bookings found for the given date'})
            return JsonResponse(data, safe=False)
        else:
            for booking in Booking.objects.all():
                data.append({
                    'name': booking.name,
                    'no_of_guests': booking.no_of_guests,
                    'time_slot': booking.time_slot,
                    'booking_date': booking.booking_date
                    })
            return JsonResponse(data, safe=False)
        
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            if Booking.objects.filter(booking_date=request.data['booking_date'], time_slot=request.data['time_slot']).exists():
                return JsonResponse({'response': 'Booking already exists for the given date and time slot'})
            serializer.save()
            
            return JsonResponse({'response': 'Booking created successfully'})
        else:
            return JsonResponse({'response': serializer.errors})
        
    def patch(self, request, *args, **kwargs):
        try:
            if 'id' not in request.data:
                return Response({'response': 'Booking id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            name = request.data.get('name')
            no_of_guests = request.data.get('no_of_guests')
            time_slot = request.data.get('time_slot')
            booking_date = request.data.get('booking_date')
            
            booking = Booking.objects.get(id=request.data['id'])
            booking.name = name if name else booking.name
            booking.no_of_guests = no_of_guests if no_of_guests else booking.no_of_guests
            booking.time_slot = time_slot if time_slot else booking.time_slot
            booking.booking_date = booking_date if booking_date else booking.booking_date
            
            booking.save()
            
            return Response({'response': 'Booking updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        try:
            if 'id' not in request.data:
                return Response({'response': 'Booking id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            print(f'Received request data: {request.data}')
            
            serializer = BookingSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({'response': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            booking = Booking.objects.get(id=request.data['id'])
            
            booking.name = request.data['name']
            booking.no_of_guests = request.data['no_of_guests']
            booking.time_slot = request.data['time_slot']
            booking.booking_date = request.data['booking_date']
            
            booking.save()
            
            print()
            print(f'Booking object: {booking}')
            
            return Response({'response': 'Booking updated successfully'}, status=status.HTTP_200_OK)
        
        except Booking.DoesNotExist:
            return Response({'response': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except ValueError as ve:
            return Response({'response': f'Invalid booking id: {ve}'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def delete(self, request, *args, **kwargs):
        try:
            if 'id' not in request.data:
                return Response({'response': 'Booking id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            booking = Booking.objects.get(id=request.data['id'])
            booking.delete()
            
            return Response({'response': 'Booking deleted successfully'}, status=status.HTTP_200_OK)
        
        except Booking.DoesNotExist:
            return Response({'response': 'Booking does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BBookingView(APIView):
    template_name = 'book.html'
    serializer_class = BookingSerializer
    
    def get(self, request):
        form = BookingForm()
        date = request.GET.get('date')
        print('date:', date)
        
        bookings = []
        bookings_raw = Booking.objects.filter(booking_date=date)
        
        if date:
            for booking in bookings_raw:
                bookings.append({
                    'name': booking.name,
                    'no_of_guests': booking.no_of_guests,
                    'time_slot': booking.time_slot,
                    'booking_date': booking.booking_date
                })
            return JsonResponse(bookings, safe=False)
        else:
            print ('No bookings found for the given date')
            pass
        return render(request, self.template_name, {'form': form, 'bookings': bookings})
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                booking = serializer.save()
                print('payload', booking)
                return Response({'response': 'Booking created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'response': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class APIMenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
    def list(self, request, *args, **kwargs):
        params = request.query_params
        queryset = Menu.objects.all()
        if 'main' in params and params.get('main') == 'true':
            print('MAIN')
            queryset = Menu.objects.filter(category_fk=1) 
            print ('debug: main', queryset)
        elif 'side' in params and params.get('side') == 'true':
            print('SIDE')
            queryset = Menu.objects.filter(category_fk=2)
            print ('debug: side', queryset)
        elif 'dessert' in params and params.get('dessert') == 'true':
            print('DESSERT')
            queryset = Menu.objects.filter(category_fk=3)
            print ('debug: dessert', queryset)
        elif 'non-alcoholic' in params and params.get('non-alcoholic') == 'true':
            print('NON-ALCOHOLIC')
            queryset = Menu.objects.filter(category_fk=4)
            print ('debug: non-alcoholic', queryset)
        elif 'alcoholic' in params and params.get('alcoholic') == 'true':
            print('ALCOHOLIC')
            queryset = Menu.objects.filter(category_fk=5)
            print ('debug: alcoholic', queryset)
        else:
            print('ALL')
            queryset = Menu.objects.all()
            print ('debug: all', queryset)
            
        serializer = MenuSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            menu_item = {
                'title': request.data.get('title'),
                'slug': request.data.get('slug'),
                'price': request.data.get('price'),
                'inventory': request.data.get('inventory'),
                'category_fk': request.data.get('category_fk'),
            } 
        
            missing_fields = [field for field, value in menu_item.items() if not value]
            
            if missing_fields:
                print ('Missing required fields:', missing_fields)
                return Response({
                    'response': f'Missing required fields: {", ".join(missing_fields)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            elif not missing_fields:
                serializer = MenuSerializer(data=menu_item)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'response': 'Menu item created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'response': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        except ValueError as ve:
            return Response({'response': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        


class BMenuView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu.html'

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
            queryset = Menu.objects.all()
            serializer = MenuSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
        
            context = {
                'menu_items': Menu.objects.all() 
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