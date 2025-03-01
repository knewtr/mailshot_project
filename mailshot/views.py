from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailshot.forms import MailshotForm, MessageForm, RecipientForm
from mailshot.models import Attempt, Mailshot, Message, Recipient


def home_view(request):
    mailshots = Mailshot.objects.count()
    started_mailshots = Mailshot.objects.filter(status="started").count()
    recipients = Recipient.objects.count()
    context = {
        "mailshots": mailshots,
        "started_mailshots": started_mailshots,
        "recipients": recipients,
    }
    return render(request, "mailshot/home.html", context)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    fields = ("email", "name", "comment")
    success_url = reverse_lazy("mailshot:recipient_list")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mailshot/recipient_list.html"

    def get_queryset(self):
        if not self.request.user.has_perm("can_view_recipient_list"):
            return Mailshot.caching(
                super().get_queryset(), self.model, self.request.user
            )
        else:
            return Mailshot.caching(super().get_queryset(), self.model)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    fields = ("email", "name", "comment")

    def get_success_url(self):
        return reverse_lazy("mailshot:recipient_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return RecipientForm
        raise PermissionDenied


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailshot/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailshot:recipient_list")


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ("theme", "content")
    success_url = reverse_lazy("mailshot:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailshot/message_list.html"

    def get_queryset(self):
        if not self.request.user.has_perm("can_view_message_list"):
            return Mailshot.caching(
                super().get_queryset(), self.model, self.request.user
            )
        else:
            return Mailshot.caching(super().get_queryset(), self.model)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ("theme", "content")

    def get_success_url(self):
        return reverse_lazy("mailshot:message_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return MessageForm
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailshot/message_confirm_delete.html"
    success_url = reverse_lazy("mailshot:message_list")


class MailshotCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ("first_mailshot", "last_mailshot", "status", "message", "recipient")
    success_url = reverse_lazy("mailshot:mailshot_list")

    def form_valid(self, form):
        mailshot = form.save()
        user = self.request.user
        mailshot.owner = user
        mailshot.save()
        return super().form_valid(form)


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

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return MailshotForm
        raise PermissionDenied

    @staticmethod
    def stop_mailshot(request, pk):
        stopped_mailshot = Mailshot.objects.get(pk=pk)
        if not request.user.has_per("mailshot.can_stop_mailshot"):
            raise PermissionDenied
        else:
            stopped_mailshot.status = "completed"
            stopped_mailshot.save()
        return redirect(reverse("mailshot:mailshot_list"))


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
            if attempt.status == "success":
                successful += 1
                mailshot_count += attempt.mailshot.recipients.count()
            if attempt.status == "failure":
                failed += 1

        context["successful"] = successful
        context["failed"] = failed
        context["mailshot_count"] = mailshot_count
        context["attempts"] = attempts
        return context
