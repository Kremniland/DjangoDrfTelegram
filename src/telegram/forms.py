from django import forms

from .models import Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = (
            'text',
            'chat_id',
            'user_id',
        )
        widgets = {
            'text': forms.Textarea,
        }