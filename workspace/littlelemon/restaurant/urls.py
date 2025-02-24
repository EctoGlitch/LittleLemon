from django.urls import path
from . import views
from .views import HomeView



urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    path('book-api/', views.APIBookview.as_view(), name='api-book'),
    path('book/', views.BBookingView.as_view(), name='book'),
    
    
    path('menu/', views.BMenuView.as_view(), name='menu'),
    path('menu-api/' , views.APIMenuView.as_view(), name='menu-api'),
    
    path('menu/<slug:slug>', views.SingleMenuItemView.as_view(), name='menu-detail'),
]