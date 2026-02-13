from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('orders/<int:order_id>/items/', views.OrderItemsApiView.as_view(), name='order-items'),
]
