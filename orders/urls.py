from django.urls import path
from .views import OrderListView, OrderDetailEach,AddProductToOrderView,PlaceOrderAPIView


urlpatterns = [
    path('',OrderListView.as_view(),name='orders-list'),
    path('<int:pk>/',OrderDetailEach.as_view(), name='order-detail'),
    path('add-product/',AddProductToOrderView.as_view(),name = 'add_product'),
    path('place_order/',PlaceOrderAPIView.as_view(),name="place-order")
]








