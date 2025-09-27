from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from oauth2_provider.models import Application
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def auth_info(request):
    """
    Provides information about authentication methods and available endpoints.
    """
    return Response({
        'message': 'Authentication Information',
        'authentication_methods': [
            'OAuth2 Bearer Token',
            'Session Authentication',
            'Token Authentication'
        ],
        'endpoints': {
            'oauth2': {
                'token': '/oauth/token/',
                'revoke': '/oauth/revoke_token/',
                'authorize': '/oauth/authorize/',
                'applications': '/oauth/applications/'
            },
            'api': {
                'customers': '/api/v1/customers/',
                'orders': '/api/v1/orders/'
            }
        },
        'how_to_authenticate': {
            'oauth2': {
                'step1': (
                    'Create an OAuth2 application via Django admin or API'
                ),
                'step2': ('Use client credentials to get access token from '
                          '/oauth/token/'),
                'step3': ('Include token in Authorization header: '
                          'Bearer <token>'),
                'example': 'Authorization: Bearer your_access_token_here'
            },
            'session': {
                'step1': 'Login via Django admin or create session',
                'step2': 'Include session cookie in requests',
                'note': 'Useful for web applications'
            },
            'token': {
                'step1': 'Create a token via Django admin or API',
                'step2': ('Include token in Authorization header: '
                          'Token <token>'),
                'example': 'Authorization: Token your_token_here'
            }
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_oauth_application(request):
    """
    Create a new OAuth2 application for testing purposes.
    """
    try:
        # Get or create a default user for the application
        user, created = User.objects.get_or_create(
            username='api_user',
            defaults={
                'email': 'api@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )

        # Create OAuth2 application
        app, created = Application.objects.get_or_create(
            name='API Test Application',
            defaults={
                'user': user,
                'client_type': Application.CLIENT_CONFIDENTIAL,
                'authorization_grant_type': (
                    Application.GRANT_CLIENT_CREDENTIALS
                ),
            }
        )

        return Response({
            'message': 'OAuth2 Application created successfully',
            'application': {
                'id': app.id,
                'name': app.name,
                'client_id': app.client_id,
                'client_secret': app.client_secret,
            },
            'instructions': {
                'step1': f'Use client_id: {app.client_id}',
                'step2': f'Use client_secret: {app.client_secret}',
                'step3': ('POST to /oauth/token/ with '
                          'grant_type=client_credentials'),
                'step4': ('Use the returned access_token in '
                          'Authorization header')
            },
            'example_request': {
                'url': '/oauth/token/',
                'method': 'POST',
                'data': {
                    'grant_type': 'client_credentials',
                    'client_id': app.client_id,
                    'client_secret': app.client_secret,
                }
            }
        }, status=(status.HTTP_201_CREATED if created
                   else status.HTTP_200_OK))

    except Exception as e:
        logger.error(f'Error creating OAuth application: {e}')
        return Response({
            'error': 'Failed to create OAuth application',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
