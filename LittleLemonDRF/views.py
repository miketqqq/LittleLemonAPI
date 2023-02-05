from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from .models import Category, MenuItem, Cart, Order, OrderItem
from LittleLemonDRF.serializers import *
#from LittleLemonDRF.serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .utils import CustomPagination, IsDeliveryCrew
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
        if user.is_staff: 
            return Cart.objects.all()           
        else:
            return Cart.objects.filter(user=user).select_related('menuitem')


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to place orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['user']
    filterset_fields = ['user', 'status', 'delivery_crew',]

    pagination_class = CustomPagination

    def get_queryset(self):
        #get user's order
        user = self.request.user

        #admin can get all orders
        if user.is_staff:
            return Order.objects.all().prefetch_related('orderitem')
        
        #Delivery_crew can only get assigned orders
        elif user.groups.filter(name='Delivery_crew').exists():
            return Order.objects.filter(delivery_crew=user).prefetch_related('orderitem')
        
        #user returns its own orders
        else:
            return Order.objects.filter(user=user).prefetch_related('orderitem')

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'update':
            permission_classes = [permissions.IsAdminUser | IsDeliveryCrew]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update':
            user = self.request.user
            if user.is_staff: 
                self.serializer_class = ManagerOrderSerializer
            elif user.groups.filter(name='Delivery_crew').exists():
                self.serializer_class = CrewOrderSerializer

        return super().get_serializer_class()

    def create(self, request):
        user = request.user

        #get all items from cart
        cart = Cart.objects.filter(user=user)
        if not cart:
            content = {'message': "no item in cart"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            #create an order instance for orderitem to reference
            order = Order.objects.create(
                user=user,
                date=date.today()
            )
            order_total = 0

            #transform all cart items to order items
            for cart_item in cart:
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
        except Exception:
            raise Exception
        else:
            #clear all cart items only if no error in creating an order
            Cart.objects.all().delete()

        return Response(self.serializer_class(order).data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        order_items = instance.orderitem.all()

        #return order items instead of order
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    


    