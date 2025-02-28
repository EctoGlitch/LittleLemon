"""
URL configuration for littlelemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant import views
from restaurant.views import HomeView, logoutView, APILoginView, CsrfTestView
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static


# routers
router = DefaultRouter()
router.register(r'tables', views.BookingViewSet)


urlpatterns = [
    # Base paths
    path('',  HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('restaurant.urls')),
    
    # Restaurant paths
    path('restaurant/', include('restaurant.urls')),
    path('restaurant/booking/', include(router.urls)),
    
    # Authentication paths
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api-token-auth/', obtain_auth_token),
    

    path('login/', views.BLoginView.as_view(), name='login'),
    path('api/login/', views.APILoginView.as_view(), name='api-login'),
    
    path('signup/', views.BSignUpView.as_view(), name='signup'),
    path('api/signup/', views.APISignUpView.as_view(), name='api-signup'),
    
    path('logout/', logoutView, name='logout'),
    path('csrf-test/', views.CsrfTestView.as_view(), name='csrf_test'),
    
  #force static files to be served no mater what
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
