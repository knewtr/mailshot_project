from django.contrib import admin

from mailshot.models import Recipient, Message, Mailshot


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "comment")
    search_fields = ("name",)
    ordering = ("email",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("theme", "content")
    search_fields = ("theme",)
    ordering = ("theme",)

@admin.register(Mailshot)
class MailshotAdmin(admin.ModelAdmin):
    list_display = ("first_mailshot", "last_mailshot", "status", "message", "recipient")
    list_filter = ("status",)
    search_field = ("message",)