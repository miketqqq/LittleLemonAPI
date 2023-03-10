from django.urls import path, include
from rest_framework import routers
from LittleLemonDRF import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'menu-items', views.MenuItemViewSet)
router.register(r'cart/menu-items', views.CartViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'groups/manager/users', views.ManagerViewSet)
router.register(r'groups/delivery-crew/users', views.CrewViewSet)
#router.register(r'orderitem', views.OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]