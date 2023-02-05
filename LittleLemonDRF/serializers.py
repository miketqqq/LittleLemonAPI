from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'groups']
        read_only_fields = ['groups']

        
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
    orderitem = serializers.StringRelatedField(many=True, read_only=True)
    delivery_crew = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['orderitem', 'status', 'total', 'date']
        

class ManagerOrderSerializer(OrderSerializer):
    delivery_crew = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.filter(groups__name='Delivery_crew'),
    )
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total', 'date']

class CrewOrderSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total', 'date']


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField(read_only=True)
    status = serializers.BooleanField(source='order.status')

    class Meta:
        model = OrderItem
        fields = ['id', 'status', 'menuitem', 'quantity', 'unit_price', 'price']