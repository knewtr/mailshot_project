from django.urls import path

from mailshot.apps import MailshotConfig
from mailshot.models import Mailshot
from mailshot.views import (
    RecipientCreateView,
    RecipientListView,
    RecipientDetailView,
    RecipientUpdateView,
    RecipientDeleteView,
)

app_name = MailshotConfig.name

urlpatterns = [
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/list/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient/detail/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipient/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipient/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
]
