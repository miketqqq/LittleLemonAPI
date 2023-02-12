from django.test import TestCase
from restaurant.models import *
from restaurant.serializers import *


# Create your tests here.
class MenuViewTest(TestCase):

    def setUp(self) -> None:
        instance = [
            {'title':"Chocolate", 'price':10, 'inventory':10},
            {'title':"IceCream", 'price':20, 'inventory':30}
        ]
        Menu.objects.create(**instance[0])
        Menu.objects.create(**instance[1])
        return super().setUp()
    
    def test_getall(self):
        items = Menu.objects.all()
        serialized = MenuItemsSerializer(items, many=True)
        self.assertEqual(serialized.data[0]['id'], 1)
