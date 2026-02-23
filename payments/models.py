from django.db import models
import uuid

class Payment(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    transaction_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('SUCCESS', 'Success'),
            ('FAILED', 'Failed')
        ],
        default='PENDING'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('COD', 'Cash on Delivery'),
            ('STRIPE', 'Stripe')
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.payment_status}"


