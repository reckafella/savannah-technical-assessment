from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from oauth2_provider.models import Application, AccessToken
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from unittest.mock import patch

from app.models.customers.models import Customer
from app.models.orders.models import Order


class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name='John Doe',
            phone_number='+254722000001',
            email='john.doe@example.com',
            code='CUST001'
        )

    def test_customer_model_creation(self):
        self.assertEqual(self.customer.name, 'John Doe')
        self.assertEqual(self.customer.phone_number, '+254722000001')
        self.assertEqual(self.customer.email, 'john.doe@example.com')
        self.assertEqual(self.customer.code, 'CUST001')

    def tearDown(self) -> None:
        self.customer.delete()
        return super().tearDown()


class CustomerAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.application = Application.objects.create(
            name='Test Application',
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE
        )

        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=3600),
            token='test-token',
            application=self.application,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token.token
        )

    def test_customer_creation(self):
        # Clear any existing customers first
        Customer.objects.all().delete()

        # Create initial customer
        Customer.objects.create(
            name='John Doe',
            phone_number='+254722000001',
            email='john.doe@example.com',
            code='CUST001',
            customer_id='CUST001'
        )

        url = reverse('customer-list-create')
        data = {
            'name': 'Jane Doe',
            'phone_number': '+254722000002',
            'email': 'jane.doe@example.com',
            'code': 'CUST002',
            'customer_id': 'CUST002'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Customer.objects.get(code='CUST002').name,
                         'Jane Doe')
        self.assertEqual(Customer.objects.get(code='CUST002').phone_number,
                         '+254722000002')
        self.assertEqual(Customer.objects.get(code='CUST002').email,
                         'jane.doe@example.com')
        self.assertEqual(Customer.objects.get(code='CUST002').code,
                         'CUST002')

    def test_customer_list(self):
        # Clear any existing customers first
        Customer.objects.all().delete()

        # Create exactly two customers for the list test
        Customer.objects.create(
            name='John Doe',
            phone_number='+254722000001',
            email='john.doe@example.com',
            code='CUST001',
            customer_id='CUST001'
        )
        Customer.objects.create(
            name='Jane Doe',
            phone_number='+254722000002',
            email='jane.doe@example.com',
            code='CUST002',
            customer_id='CUST002'
        )

        url = reverse('customer-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            customers = response.data['results']
        else:
            customers = response.data

        self.assertEqual(len(customers), 2)
        # Check the first customer (John Doe)
        john_customer = next(c for c in customers if c['code'] == 'CUST001')
        self.assertEqual(john_customer['name'], 'John Doe')
        self.assertEqual(john_customer['phone_number'], '+254722000001')
        self.assertEqual(john_customer['email'], 'john.doe@example.com')
        self.assertEqual(john_customer['code'], 'CUST001')
        # Check the second customer (Jane Doe)
        jane_customer = next(c for c in customers if c['code'] == 'CUST002')
        self.assertEqual(jane_customer['name'], 'Jane Doe')
        self.assertEqual(jane_customer['phone_number'], '+254722000002')
        self.assertEqual(jane_customer['email'], 'jane.doe@example.com')
        self.assertEqual(jane_customer['code'], 'CUST002')

    def test_customer_detail(self):
        Customer.objects.create(
            name='Jane Doe',
            phone_number='+254722000002',
            email='jane.doe@example.com',
            code='CUST002',
            customer_id='CUST002'
        )
        url = reverse('customer-detail',
                      args=[Customer.objects.get(code='CUST002').id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Jane Doe')
        self.assertEqual(response.data['phone_number'], '+254722000002')
        self.assertEqual(response.data['email'], 'jane.doe@example.com')
        self.assertEqual(response.data['code'], 'CUST002')

    def tearDown(self) -> None:
        self.user.delete()
        self.application.delete()
        self.access_token.delete()
        return super().tearDown()


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name='John Doe',
            phone_number='+254722000001',
            email='john.doe@example.com',
            code='CUST001'
        )

    def test_order_model_creation(self):
        order = Order.objects.create(
            customer=self.customer,
            item='Laptop',
            amount=100000.00,
            status='pending'
        )
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.item, 'Laptop')
        self.assertEqual(order.amount, 100000.00)
        self.assertEqual(order.status, 'pending')


class OrderAPITest(APITestCase):
    def setUp(self):
        # Clear any existing data
        Order.objects.all().delete()
        Customer.objects.all().delete()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.application = Application.objects.create(
            name='Test Application',
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE
        )

        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=3600),
            token='test-token',
            application=self.application,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token.token
        )

        # Create a customer for order tests
        self.customer = Customer.objects.create(
            name='John Doe',
            phone_number='+254722000001',
            email='john.doe@example.com',
            code='CUST001',
            customer_id='CUST001'
        )

    @patch('app.views.orders.views.send_order_notification')
    def test_order_creation(self, mock_send_order_notification):
        url = reverse('order-list-create')
        data = {
            'customer_code': 'CUST001',
            'item': 'Laptop',
            'amount': 100000.00,
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        mock_send_order_notification.assert_called_once()
        self.assertEqual(
            Order.objects.get(id=response.data['id']).customer, self.customer)
        self.assertEqual(
            Order.objects.get(id=response.data['id']).item, 'Laptop')
        self.assertEqual(
            Order.objects.get(id=response.data['id']).amount, 100000.00)
        self.assertEqual(
            Order.objects.get(id=response.data['id']).status, 'pending')

    def tearDown(self) -> None:
        self.user.delete()
        self.application.delete()
        self.access_token.delete()
        return super().tearDown()
