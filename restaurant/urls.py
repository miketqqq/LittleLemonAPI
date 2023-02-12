from django.urls import path, include
from rest_framework import routers
from restaurant import views


router = routers.DefaultRouter()
router.register(r'menu', views.MenuItemsViewSet)
router.register(r'booking/tables', views.BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('index', views.index, name='home'),

]
