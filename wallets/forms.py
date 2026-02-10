from django import forms
from django.core.exceptions import ValidationError
from .models import Wallet

class WalletForm(forms.ModelForm):

    class Meta:
        model = Wallet
        fields = ['wallet_type', 'card_type', 'title', 'currency', 'balance', 'created_at']
        widgets = {
            'created_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': False
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        wallet_type = cleaned_data.get('wallet_type')
        card_type = cleaned_data.get('card_type')
        title = cleaned_data.get('title')
        currency = cleaned_data.get('currency')

        user = self.initial.get('user') or (self.instance.user if self.instance.pk else None)

        if not user:
            return cleaned_data

        qs = Wallet.objects.filter(
            user=user,
            is_deleted=False
        )
        
        # Exclude current instance if updating
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        # -------- NAQD --------
        if wallet_type == 'naqd':
            exists = qs.filter(
                wallet_type='naqd',
                currency=currency
            ).exists()

            if exists:
                raise ValidationError(
                    'Bu valyutada naqd hamyon allaqachon mavjud'
                )

        # -------- KARTA --------
        elif wallet_type == 'karta':
            exists = qs.filter(
                wallet_type='karta',
                card_type=card_type,
                title=title,
                currency=currency
            ).exists()

            if exists:
                raise ValidationError(
                    'Bunday karta hamyoni allaqachon mavjud'
                )

        return cleaned_data
