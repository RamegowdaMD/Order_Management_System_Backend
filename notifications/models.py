from django.db import models
from orders.models import Order
from django.conf import settings

class Notification(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'notifications_details'
    )


    notification_type = models.CharField(max_length = 50 , choices = [('ORDER_CONFIRMATION','Order Confirmation'),('PAYMENT_SUCCESS','Payment_Success'),('ORDER_CANCELLED','Order_cancelled')])
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.notification_type}"



