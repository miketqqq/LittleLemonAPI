from django.urls import path, include
from rest_framework import routers
from LittleLemonDRF import views

router = routers.DefaultRouter()

router.register(r'category', views.CategoryViewSet)
router.register(r'menuitem', views.MenuItemViewSet)
router.register(r'cart/menu-items', views.CartViewSet)
router.register(r'order', views.OrderViewSet)
#router.register(r'orderitem', views.OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
