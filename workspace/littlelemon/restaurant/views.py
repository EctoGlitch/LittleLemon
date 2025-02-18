from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import generics
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
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import  login, logout
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import parser_classes
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

# Create your views here.

def print_test():
    data = 'error in data'
    print(data)

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'


# class login_view(TemplateView):
#     template_name = 'login.html'

class login_view(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
            else:
                print('Invalid username or password')  # Debugging statement
                return render(request, 'login.html', {'error': 'Invalid credentials'})
                
        return render(request, 'login.html', {'form': form})

class signup_view(SuccessMessageMixin, generic.FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    success_message = 'You have successfully registered!'

    def form_valid(self, form):
        try:
            print("Form is valid")
            user = form.save()
            login(self.request, user)
            return super().form_valid(form)
        
        except Exception as e:
            print(f"Error saving user: {e}")
            context = self.get_context_data(form=form)
            context['error_message'] = str(e)
            return self.render_to_response(context)

    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)
        context = self.get_context_data(form=form)
        context['error_message'] = form.errors.as_json()
        return self.render_to_response(context)

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
                token = Token.objects.get(user=user)
                token.delete()
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



