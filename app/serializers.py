from rest_framework import serializers

from app.models.customers.models import Customer
from app.models.orders.models import Order


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'phone_number',
                  'email', 'customer_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        if Customer.objects.filter(code=value).exists():
            raise serializers.ValidationError(
                'Code already exists')
        return value


class OrderSerializer(serializers.ModelSerializer):
    customer_details = CustomerSerializer(source='customer', read_only=True)
    customer_code = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_details',
                  'customer_code', 'item', 'order_date', 'amount',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at',
                            'order_date', 'customer']

    def validate_customer_code(self, value):
        if not Customer.objects.filter(code=value).exists():
            raise serializers.ValidationError(
                'Customer code does not exist')
        return value

    def validate_customer(self, value):
        if not Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                'Customer does not exist')
        return value

    def create(self, validated_data):
        customer_code = validated_data.pop('customer_code')
        customer = Customer.objects.get(code=customer_code)
        validated_data['customer'] = customer
        return super().create(validated_data)
