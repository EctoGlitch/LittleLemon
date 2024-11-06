from django.test import TestCase
from restaurant.models import Booking
from restaurant.serializers import BookingSerializer
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
        
class BookingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.booking = Booking.objects.create(name="Dexter", no_of_guests=10, time_slot=10, booking_date='2021-01-01')
        
    # def test_getall_book_list(self):
    #     response = self.client.get(reverse('booking-list'))
    #     bookings = Booking.objects.all()
    #     serializer = BookingSerializer(bookings, many=True)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, serializer.data)
        
    def test_getall_booking(self):
        response = self.client.get(reverse('book'))
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)