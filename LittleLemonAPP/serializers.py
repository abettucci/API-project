from .models import MenuItem, Category, Order, Cart
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta():
        model = MenuItem
        fields = ['id','title','price','inventory','category','category_id']

        # extra_kwargs = { 
        #     'price' : {'min_value' : 2},
        #     'inventory' : {'min_value':0}
        #     }

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        order = Order

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        cart = Cart