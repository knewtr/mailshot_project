from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from mailshot.models import Mailshot, Message, Recipient


class RecipientCreateView(CreateView):
    model = Recipient
    fields = ("email", "name", "comment")
    success_url = reverse_lazy("mailshot:recipient_list")


class RecipientListView(ListView):
    model = Recipient
    template_name = "mailshot/recipient_list.html"


class RecipientDetailView(DetailView):
    model = Recipient


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ("email", "name", "comment")

    def get_success_url(self):
        return reverse_lazy("mailshot:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "mailshot/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailshot:recipient_list")


class MessageCreateView(CreateView):
    model = Message
    fields = ("theme", "content")
    success_url = reverse_lazy("mailshot:message_list")


class MessageListView(ListView):
    model = Message
    template_name = "mailshot/message_list.html"


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = ("theme", "content")

    def get_success_url(self):
        return reverse_lazy("mailshot:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailshot/message_confirm_delete.html"
    success_url = reverse_lazy("mailshot:message_list")


class MailshotCreateView(CreateView):
    model = Message
    fields = ("first_mailshot", "last_mailshot", "status", "message", "recipient")
    success_url = reverse_lazy("mailshot:mailshot_list")


class MailshotListView(ListView):
    model = Message
    template_name = "mailshot/mailshot_list.html"


class MailshotDetailView(DetailView):
    model = Message


class MailshotUpdateView(UpdateView):
    model = Message
    fields = ("theme", "content")

    def get_success_url(self):
        return reverse_lazy("mailshot:mailshot_detail", kwargs={"pk": self.object.pk})


class MailshotDeleteView(DeleteView):
    model = Message
    template_name = "mailshot/mailshot_confirm_delete.html"
    success_url = reverse_lazy("mailshot:mailshot_list")
