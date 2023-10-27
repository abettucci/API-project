from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category, Cart, Order
from .serializers import MenuItemSerializer, CategorySerializer, OrderSerializer, CartSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator, EmptyPage
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework.renderers import TemplateHTMLRenderer

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])

def me(request):
    return Response(request.user.mail)

def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message" : "Only Manager Should See This"})
    else:
        return Response({"message" : "You are not authorized"}, 403)
    
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

def menu_items(request):
    if(request.method == 'GET'):
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title = category_name)
        if to_price:
            items = items.filter(price = to_price)
        if search:
            items = items.filter(title__contains = search) # tambien puede ser title__startswith
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page = perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)

    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.validated_data, status.HTTP_201_CREATED)

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return []
        return [IsAuthenticated()]

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer  

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return []
        return [IsAuthenticated()]
    
class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = Category
    # ordering_fields = ['price','inventory']
    # filterset_fields = ['price','inventory']
    search_fields = ['title']

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return []
        return [IsAuthenticated()] 

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return []
        return [IsAuthenticated()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price','inventory']
    filterset_fields = ['price','inventory']
    search_fields = ['title']

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return []
        return [IsAuthenticated()]

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.all().filter(user=self.request.user)