from django.urls import path

from mailshot.apps import MailshotConfig
from mailshot.views import (MessageCreateView, MessageDeleteView,
                            MessageDetailView, MessageListView,
                            MessageUpdateView, RecipientCreateView,
                            RecipientDeleteView, RecipientDetailView,
                            RecipientListView, RecipientUpdateView, home_view)

app_name = MailshotConfig.name

urlpatterns = [
    path("", home_view, name="home"),
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
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/list/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path(
        "message/<int:pk>/update/",
        MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "message/<int:pk>/delete/",
        MessageDeleteView.as_view(),
        name="message_confirm_delete",
    ),
]
