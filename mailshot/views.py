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

class RecipientDetailView(DetailView):
    model = Recipient

class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ("email", "name", "comment")

    def get_success_url(self):
        return reverse_lazy("mailshot:recipient_detail", kwargs={'pk':self.object.pk})

class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailshot:recipient_list")