from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    Category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())

    class Meta:
        model = MenuItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all())

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['price', 'unit_price']
        
    def create(self, validated_data):
        quantity = validated_data.get("quantity")
        menuitem = validated_data.get("menuitem")
        unit_price = menuitem.price
        price = quantity * unit_price
        user = self.context.get('request').user

        return Cart.objects.create(price=price, unit_price=unit_price, user=user, **validated_data)


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    delivery_crew = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(),
                                                       queryset=User.objects.filter(groups__name='delivery_crew'))

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['delivery_crew', 'status', 'total', 'date']



class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']
