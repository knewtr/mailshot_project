from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailshot.models import Message


class Command(BaseCommand):
    help = "Делает рассылку"

    def handle(self, *args, **kwargs):
        messages = Message.objects.filter(
            Q(STATUS="COMPLETE"), Q(start_date__gt=timezone.now().date())
        )
        for message in messages:

            send_mail(
                subject=Message.theme,
                message=Message.content,
                from_email=EMAIL_HOST_USER,
                recipient_list=[Message.recipient],
            )
            message.is_sent = True
            message.save()
            self.stdout.write(self.style.SUCCESS(f"Отправлено: {message.subject}"))
