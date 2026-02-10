from django import forms
from django.core.exceptions import ValidationError
from .models import Transfer
from wallets.models import Wallet


class TransferForm(forms.ModelForm):
    """O'tkazma yaratish"""

    class Meta:
        model = Transfer
        fields = ['from_wallet', 'to_wallet', 'from_amount', 'exchange_rate']
        widgets = {
            'from_wallet': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'to_wallet': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'from_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'required': True
            }),
            'exchange_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kurs (ixtiyoriy)',
                'step': '0.0000000001'
            })
        }
        labels = {
            'from_wallet': 'Qaysi hamyondan',
            'to_wallet': 'Qaysi hamyonga',
            'from_amount': 'Miqdor',
            'exchange_rate': 'Kurs'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            wallets = Wallet.objects.filter(user=self.user, is_deleted=False)
            self.fields['from_wallet'].queryset = wallets
            self.fields['to_wallet'].queryset = wallets

    def clean(self):
        cleaned_data = super().clean()
        from_wallet = cleaned_data.get('from_wallet')
        to_wallet = cleaned_data.get('to_wallet')
        from_amount = cleaned_data.get('from_amount')
        exchange_rate = cleaned_data.get('exchange_rate')

        if from_wallet and to_wallet and from_wallet.id == to_wallet.id:
            raise ValidationError('Bir xil hamyonni tanlay olmaysiz')

        if from_wallet and from_amount:
            if from_wallet.balance < from_amount:
                raise ValidationError('Balance yetarli emas')

        if from_wallet and to_wallet:
            if from_wallet.currency != to_wallet.currency and not exchange_rate:
                raise ValidationError('Exchange rate majburiy')

        return cleaned_data