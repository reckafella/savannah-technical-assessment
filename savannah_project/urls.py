"""
URL configuration for savannah_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """API root endpoint"""
    return JsonResponse({
        'message': 'Savannah Technical Assessment API',
        'version': 'v1',
        'endpoints': {
            'customers': '/api/v1/customers/',
            'orders': '/api/v1/orders/',
            'auth_info': '/api/v1/auth/info/',
            'create_app': '/api/v1/auth/create-app/',
            'oauth': {
                'token': '/oauth/token/',
                'revoke': '/oauth/revoke_token/',
            }
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('api/v1/', include('app.urls')),
    path('oauth/', include('oauth2_provider.urls',
                           namespace='oauth2_provider')),
]
