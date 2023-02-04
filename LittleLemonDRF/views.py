from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from .models import Category, MenuItem, Cart, Order, OrderItem
from LittleLemonDRF.serializers import *
#from LittleLemonDRF.serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .utils import CustomPagination
from datetime import date


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to browse all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to browse menu items at once.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated] #only manager can write

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['price']
    filterset_fields = ['Category']

    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to view and add items to cart.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #get user's cart
        user = self.request.user
        #if user.group == admin: 
        #return Cart.objects.all()
        #else:
        return Cart.objects.filter(user=user).select_related('menuitem')


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to place orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #get user's order
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)

    def create(self, request):
        user = request.user
        carts = Cart.objects.filter(user=user)
        order = Order.objects.create(
            user=user,
            date=date.today()
        )
        order_total = 0
        for cart_item in carts:
            orderitem = OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price,
            )
            orderitem.save()
            order_total += cart_item.price
        order.total = order_total
        order.save()
        Cart.objects.all().delete()
        return Response(self.serializer_class(order).data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        order_items = instance.orderitem_set.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    
    

    