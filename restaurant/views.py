from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from restaurant.models import Menu, Booking
from restaurant.serializers import MenuItemsSerializer, BookingSerializer
from django.shortcuts import render

# Create your views here. 
class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuItemsSerializer
    permission_classes = [IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

def index(request):
    return render(request, 'index.html', {})