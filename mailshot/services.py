import smtplib

from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from config.settings import CACHE_ENABLED, EMAIL_HOST_USER
from mailshot.models import Attempt, Mailshot


class MailshotService:

    @staticmethod
    def send_mailshot(request, pk):
        mailshot = Mailshot.objects.get(pk=pk)
        subject = mailshot.message.theme
        message = mailshot.message.content
        recipients = [recipient.email for recipient in mailshot.recipients.all()]

        start_mailshot = timezone.now()

        try:
            response = send_mail(
                subject, message, EMAIL_HOST_USER, recipients, fail_silently=False
            )
        except smtplib.SMTPException as e:
            MailshotService.make_attempt(
                status="failure", response=e, mailshot=mailshot
            )
        else:
            end_mailshot = timezone.now()
            MailshotService.make_attempt(
                status="success", response=response, mailshot=mailshot
            )
            MailshotService.update_status(
                mailshot=mailshot,
                start_mailshot=start_mailshot,
                end_mailshot=end_mailshot,
            )
        finally:
            return redirect(reverse("mailshot:mailshot_list"))

    @staticmethod
    def make_attempt(status, response, mailshot):
        attempt = Attempt.objects.create(
            status=status, response=response, mailshot=mailshot
        )
        attempt.save()

    @staticmethod
    def update_status(mailshot, start_mailshot, end_mailshot):
        mailshot.start_mailshot = timezone.localtime(start_mailshot)
        mailshot.end_mailshot = timezone.localtime(end_mailshot)
        mailshot.status = "completed"
        mailshot.save()

    @staticmethod
    def caching(queryset, model, user=None):
        if not CACHE_ENABLED:
            return queryset.filter(owner=user)
        key = str(model) + "_list"
        objects = cache.get(key)
        if objects is not None:
            return objects
        objects = queryset.filter(owner=user)
        cache.set(key, objects, 60 * 1)
        return objects
