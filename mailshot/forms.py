from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm

from mailshot.models import Message, Recipient, Mailshot


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
        fields = ("title", "content")


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipient
        fields = ("email", "name", "comment")


class MailshotForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailshot
        fields = ("first_mailshot", "last_mailshot", "status", "message", "recipient")
