from django.contrib import admin

from mailshot.models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "comment")
    search_fields = ("name",)
    ordering = ("email",)
