from django.urls import path
from . import views

# son todos URL de /api/...
urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('categories', views.CategoriesView.as_view()),
    path('categories/<int:pk>', views.SingleCategoryView.as_view()),
    path('cart', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    # path('orders/<int:pk>', views.SingleOrderView.as_view()), #para una order id
    path('manager-view/', views.manager_view),
    # path('welcome', views.welcome),
    # path('groups/delivery-crew/users', views.delivery_crew),
    path('me/', views.me),
    # path('groups/manager/users', views.managers),
    # path('groups/manager/users/<int:pk>', views.managers) #user id
    # path('roles', views.roles)
]

