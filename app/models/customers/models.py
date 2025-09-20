from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=255, validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message=('Phone number must include'
                     'the country code e.g +254 for Kenya.'
                     'Up to 15 digits allowed.'))])

    email = models.EmailField(max_length=255, unique=True)
    customer_id = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.phone_number} - {self.email}'

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        unique_together = ('phone_number', 'email', 'code')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
        ]
