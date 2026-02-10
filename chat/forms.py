from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Message


class MessageForm(forms.ModelForm):
    """Chat xabar yuborish"""

    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Xabar yozing...'),
                'rows': '1',
                'style': 'resize: none;',
                'data-i18n': 'placeholder_message'
            }),
        }
        labels = {
            'text': ''
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')

        if not text or len(text.strip()) == 0:
            raise ValidationError(_('Xabar bo\'sh bo\'lishi mumkin emas'))

        return text.strip()