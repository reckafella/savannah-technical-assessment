from django.urls import path
from app.views.orders.views import OrderListCreateView, OrderDetailView
from app.views.customers.views import (
    CustomerListCreateView, CustomerDetailView
)


urlpatterns = [
    path('customers', CustomerListCreateView.as_view(),
         name='customer-list-create'
    ),
    path('customers/<int:pk>', CustomerDetailView.as_view(),
         name='customer-detail'
    ),
    path('orders', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<uuid:pk>', OrderDetailView.as_view(), name='order-detail'),
]