from django.db import models
from django.conf import settings
from django.db.models import Sum
from products.models import Product

class Order(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'orders'
    )

    status = models.CharField(max_length=255 , choices=[('PENDING','pending'),('CONFIRMED','confirmed'),('DELIVERED','delivered')],default='PENDING')
    
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00)
    
    address = models.TextField(max_length=2000)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def update_total(self):
        total = self.items.aggregate(
            total=Sum('price')
        )['total'] or 0

        self.total_price = total
        self.save(update_fields=['total_price'])

    def __str__(self):
        return f"order #{self.id}-{self.user.username}"



class OrderItem(models.Model):
    order= models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        related_name = 'items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete = models.CASCADE,
        related_name = 'order_items'
    )

    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00
    )

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)

        self.order.update_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)

        order.update_total()

    def __str__(self):
        return f"Product Name {self.product.name} - quantity {self.quantity}"

    