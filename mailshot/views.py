from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    TemplateView
)

from mailshot.models import Mailshot, Message, Recipient, Attempt


def home_view(request):
    messages = Message.objects.all()
    context = {
        "meassages": messages,
    }
    return render(request, "mailshot/home.html", context)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    fields = ("email", "name", "comment")
    success_url = reverse_lazy("mailshot:recipient_list")


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mailshot/recipient_list.html"


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    fields = ("email", "name", "comment")

    def get_success_url(self):
        return reverse_lazy("mailshot:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailshot/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailshot:recipient_list")


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ("theme", "content")
    success_url = reverse_lazy("mailshot:message_list")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailshot/message_list.html"


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ("theme", "content")

    def get_success_url(self):
        return reverse_lazy("mailshot:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailshot/message_confirm_delete.html"
    success_url = reverse_lazy("mailshot:message_list")


class MailshotCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ("first_mailshot", "last_mailshot", "status", "message", "recipient")
    success_url = reverse_lazy("mailshot:mailshot_list")


class MailshotListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailshot/mailshot_list.html"


class MailshotDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MailshotUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ("theme", "content")

    def get_success_url(self):
        return reverse_lazy("mailshot:mailshot_detail", kwargs={"pk": self.object.pk})


class MailshotDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailshot/mailshot_confirm_delete.html"
    success_url = reverse_lazy("mailshot:mailshot_list")

class StatisticsView(TemplateView):
    template_name = "mailshot/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        mailshots = Mailshot.objects.filter(owner=user)
        attempts = Attempt.objects.filter(mailshot__in=mailshots)
        print(attempts)

        successful = 0
        failed = 0
        mailshot_count = 0

        for attempt in attempts:
            if attempt.status == 'success':
                successful += 1
                mailshot_count += attempt.mailshot.recipients.count()
            if attempt.status == 'failure':
                failed += 1

        context['successful'] = successful
        context['failed'] = failed
        context['mailshot_count'] = mailshot_count
        context['attempts'] = attempts
        return context

