from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('products/', product, name='products'),
    path('customer/<str:pk>/', customer, name='customer'),
    path('create_order/<str:pk>/', create_order, name='create-order'),
    path('update_order/<str:pk>/', update_order, name='update-order'),
    path('delete_order/<str:pk>/', delete_order, name='delete-order'),
    path('registration/', register_page, name='registration'),
]
