from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from .models import Menu, Booking
from .forms import BookingForm
from django.contrib.auth.models import User
from .serializers import MenuSerializer, BookingSerializer, UserSerializer
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
import json

# Create your views here.

def print_test():
    data = 'error in data'
    print(data)

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

@method_decorator(csrf_exempt, name='dispatch')
@parser_classes([JSONParser])
class BookView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            date = request.GET.get('date')
            bookings = Booking.objects.filter(booking_date=date)
            data = []
            ['name', 'no_of_guests', 'time_slot',  'booking_date']
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
            print("Received data:", request.data)
            
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                booking = serializer.save()
                print("Booking created:", booking)
                return JsonResponse(serializer.data, status=201)
            
            print("Validation errors:", serializer.errors)
            return JsonResponse(serializer.errors, status=400)
            
        except Exception as e:
            print("Unexpected error:", str(e))
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    

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
    

