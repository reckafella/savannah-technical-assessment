from django.contrib import admin

from app.models.customers.models import Customer
from app.models.orders.models import Order

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
