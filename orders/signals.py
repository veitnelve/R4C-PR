from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from robots.models import Robot
from .models import Order


@receiver(post_save, sender=Robot)
def send_email_to_waiting_customer(sender, instance, created, **kwargs):
    if created:
        waiting_customers = Order.objects.filter(robot_serial=instance.serial)
        recipients = [order.customer.email for order in waiting_customers]
        subject = f'Робот модели {instance.serial} доступен!'
        message = f'Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.serial[:2]}, версии {instance.serial[3:]}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipients)

