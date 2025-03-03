from django.forms import BooleanField, ModelForm

from mailshot.models import Mailshot, Message, Recipient


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = ("theme", "content")


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipient
        fields = ("email", "name", "comment")


class MailshotForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailshot
        fields = ("start_mailshot", "end_mailshot", "status", "message", "recipients")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MailshotForm, self).__init__(*args, **kwargs)
        self.fields["end_mailshot"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local", 'class': 'form-control'})
        self.fields["start_mailshot"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local", 'class': 'form-control'})

        if user:
            self.fields['message'].queryset = Message.objects.filter(owner=user)
            self.fields['recipients'].queryset = Recipient.objects.filter(owner=user)