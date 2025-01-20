from django.urls import path

from mailshot.apps import MailshotConfig
from mailshot.views import (
    RecipientCreateView,
    RecipientDeleteView,
    RecipientDetailView,
    RecipientListView,
    RecipientUpdateView,
)

app_name = MailshotConfig.name

urlpatterns = [
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/list/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path(
        "recipient/<int:pk>/update/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="recipient_confirm_delete",
    ),
]
