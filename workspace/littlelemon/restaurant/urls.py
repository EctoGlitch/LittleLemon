from django.urls import path
from . import views
from .views import HomeView, BookView



urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('book/', BookView.as_view(), name='book'),
    path('menu/', views.MenuItemView.as_view(), name='menu-list'),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view()),
]