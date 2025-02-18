from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from mailshot.models import Message
from config.settings import EMAIL_HOST_USER


class Command(BaseCommand):
    help = "Делает рассылку"

    def handle(self, *args, **kwargs):
        messages = Message.objects.filter(is_sent = False)
        for message in messages:
            send_mail(
                subject=Message.theme,
                message=Message.content,
                from_email=EMAIL_HOST_USER,
                recipient_list=['to@example.com'],
            )
            message.is_sent = True
            message.save()
            self.stdout.write(self.style.SUCCESS(f'Отправлено: {message.subject}'))