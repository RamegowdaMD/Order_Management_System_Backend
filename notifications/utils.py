from .models import Notification
from .services import BrevoEmailService


def send_order_notification(user, notification_type, message):

    
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message
    )

    BrevoEmailService.send_email(
        to_email=user.email,
        subject=notification_type.replace("_", " "),
        content=message
    )

