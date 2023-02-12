from django.contrib.auth.models import User
from rest_framework import serializers
from restaurant.models import Menu, Booking


class MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'