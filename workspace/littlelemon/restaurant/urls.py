from django.urls import path
from . import views
from .views import HomeView, BookView



urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('book/', BookView.as_view(), name='book'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('menu/<slug:slug>', views.SingleMenuItemView.as_view(), name='menu-detail'),
]