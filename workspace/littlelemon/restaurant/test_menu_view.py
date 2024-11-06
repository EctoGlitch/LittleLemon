from django.test import TestCase
from restaurant.models import Menu 
from restaurant.serializers import MenuSerializer
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu = Menu.objects.create(title="Test Menu", price=100, inventory=100)
    
    def test_getall(self):
        response = self.client.get(reverse('menu-list'))
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
