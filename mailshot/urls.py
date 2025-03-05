from django.urls import path

from mailshot.apps import MailshotConfig
from mailshot.services import MailshotService
from mailshot.views import (MailshotCreateView, MailshotDeleteView,
                            MailshotListView, MailshotUpdateView,
                            MessageCreateView, MessageDeleteView,
                            MessageDetailView, MessageListView,
                            MessageUpdateView, RecipientCreateView,
                            RecipientDeleteView, RecipientDetailView,
                            RecipientListView, RecipientUpdateView,
                            StatisticsView, home_view, MailshotDetailView,)

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
    path("mailshot/list/", MailshotListView.as_view(), name="mailshot_list"),
    path("mailshot/statistics/", StatisticsView.as_view(), name="statistics"),
    path(
        "mailshot/<int:pk>/stop/",
        MailshotUpdateView.stop_mailshot,
        name="stop_mailshot",
    ),
    path(
        "mailshot/update/<int:pk>", MailshotUpdateView.as_view(), name="mailshot_update"
    ),
    path("mailshot/create/", MailshotCreateView.as_view(), name="mailshot_create"),
    path(
        "mailshot/<int:pk>/send/", MailshotService.send_mailshot, name="send_mailshot"
    ),
    path(
        "mailshot/<int:pk>/delete/",
        MailshotDeleteView.as_view(),
        name="mailshot_confirm_delete",
    ),
    path("mailshot/<int:pk>/", MailshotDetailView.as_view(), name="mailshot_detail"),
]
