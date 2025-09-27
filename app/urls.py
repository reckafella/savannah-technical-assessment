from django.urls import path
from django.http import JsonResponse
from app.views.orders.views import OrderListCreateView, OrderDetailView
from app.views.customers.views import (
    CustomerListCreateView, CustomerDetailView
)
from app.views.auth.views import auth_info, create_oauth_application


def api_v1_root(request):
    """API v1 root endpoint"""
    return JsonResponse({
        'message': 'Savannah Technical Assessment API v1',
        'endpoints': {
            'customers': '/api/v1/customers/',
            'orders': '/api/v1/orders/',
            'auth': {
                'info': '/api/v1/auth/info/',
                'create_app': '/api/v1/auth/create-app/'
            }
        }
    })


urlpatterns = [
    path('', api_v1_root, name='api-v1-root'),
    path('customers/', CustomerListCreateView.as_view(),
         name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(),
         name='customer-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('auth/info/', auth_info, name='auth-info'),
    path('auth/create-app/', create_oauth_application,
         name='create-oauth-app'),
]
