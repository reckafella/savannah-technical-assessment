from django.db import models
import uuid

from app.models.customers.models import Customer


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending'
        PROCESSING = 'processing'
        COMPLETED = 'completed'
        CANCELLED = 'cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, choices=OrderStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Order {self.id} - for {self.customer.name} - {self.status}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['order_date']),
        ]
