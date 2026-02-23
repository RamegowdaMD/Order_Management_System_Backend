from celery import shared_task
from .models import Notification
from .services import BrevoEmailService


@shared_task
def send_notification_task(user_id, notification_type , message , email):

    Notification.objects.create(user_id = user_id, notification_type = notification_type , message = message)


    BrevoEmailService.send_email(to_email = email , subject = notification_type.replace("_",""),content = message)
