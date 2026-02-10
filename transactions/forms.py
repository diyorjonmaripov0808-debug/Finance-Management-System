from django import forms
from django.core.exceptions import ValidationError
from .models import Transaction
from wallets.models import Wallet
from categories.models import Category


class IncomeForm(forms.ModelForm):
    """Kirim qo'shish formasi"""

    class Meta:
        model = Transaction
        fields = ['wallet', 'category', 'amount', 'currency', 'exchange_rate', 'description', 'created_at']
        widgets = {
            'wallet': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'required': True
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'exchange_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kurs (ixtiyoriy)',
                'step': '0.0000000001'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Izoh (ixtiyoriy)',
                'rows': 3
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': False
            })
        }
        labels = {
            'wallet': 'Hamyon',
            'category': 'Kategoriya',
            'amount': 'Miqdor',
            'currency': 'Valyuta',
            'exchange_rate': 'Kurs',
            'description': 'Izoh',
            'created_at': 'Yaratilgan vaqt'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


        if self.user:
            wallets = Wallet.objects.filter(user=self.user, is_deleted=False)
            self.fields['wallet'].queryset = wallets
            # Custom choices for wallet select
            wallet_choices = [('', '---------')]
            for w in wallets:
                if w.wallet_type == 'naqd':
                    label = f"Naqd : {w.balance:.2f} ({w.currency})"
                else:
                    label = f"{w.title} ({w.card_type}): {w.balance:.2f} ({w.currency})"
                wallet_choices.append((w.pk, label))
            self.fields['wallet'].choices = wallet_choices

            self.fields['category'].queryset = Category.objects.filter(
                user=self.user,
                type='income',
                is_deleted=False
            )

    def clean(self):
        cleaned_data = super().clean()
        wallet = cleaned_data.get('wallet')
        category = cleaned_data.get('category')
        amount = cleaned_data.get('amount')
        currency = cleaned_data.get('currency')
        exchange_rate = cleaned_data.get('exchange_rate')

        if category and category.type != 'income':
            raise ValidationError('Faqat kirim kategoriyalari tanlansa bo\'ladi')

        if wallet and currency:
            if currency != wallet.currency and not exchange_rate:
                raise ValidationError('Valyuta kursi majburiy')

        # Tranzaksiya vaqti hamyon yaratilgan vaqtdan oldin bo'lmasligi kerak
        transaction_created_at = cleaned_data.get('created_at')
        if wallet and transaction_created_at:
            if transaction_created_at < wallet.created_at:
                formatted_date = wallet.created_at.strftime('%d.%m.%Y %H:%M')
                raise ValidationError(f"Tranzaksiya vaqti hamyon yaratilgan vaqtdan ({formatted_date}) oldin bo'lishi mumkin emas")

        return cleaned_data


class ExpenseForm(forms.ModelForm):
    """Chiqim qo'shish formasi"""

    class Meta:
        model = Transaction
        fields = ['wallet', 'category', 'amount', 'currency', 'exchange_rate', 'description', 'created_at']
        widgets = {
            'wallet': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'required': True
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'exchange_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kurs (ixtiyoriy)',
                'step': '0.0000000001'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Izoh (ixtiyoriy)',
                'rows': 3
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': False
            })
        }
        labels = {
            'wallet': 'Hamyon',
            'category': 'Kategoriya',
            'amount': 'Miqdor',
            'currency': 'Valyuta',
            'exchange_rate': 'Kurs',
            'description': 'Izoh',
            'created_at': 'Yaratilgan vaqt'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


        if self.user:
            wallets = Wallet.objects.filter(user=self.user, is_deleted=False)
            self.fields['wallet'].queryset = wallets
            # Custom choices for wallet select
            wallet_choices = [('', '---------')]
            for w in wallets:
                if w.wallet_type == 'naqd':
                    label = f"Naqd : {w.balance:.2f} ({w.currency})"
                else:
                    label = f"{w.title} ({w.card_type}): {w.balance:.2f} ({w.currency})"
                wallet_choices.append((w.pk, label))
            self.fields['wallet'].choices = wallet_choices

            self.fields['category'].queryset = Category.objects.filter(
                user=self.user,
                type='expense',
                is_deleted=False
            )

    def clean(self):
        cleaned_data = super().clean()
        wallet = cleaned_data.get('wallet')
        category = cleaned_data.get('category')
        amount = cleaned_data.get('amount')
        currency = cleaned_data.get('currency')
        exchange_rate = cleaned_data.get('exchange_rate')

        if category and category.type != 'expense':
            raise ValidationError('Faqat chiqim kategoriyalari tanlansa bo\'ladi')

        if wallet and currency:
            if currency != wallet.currency and not exchange_rate:
                raise ValidationError('Valyuta kursi majburiy')

        if wallet and amount and currency:
            # Hisoblash va balans tekshirish
            calculated_amount = amount
            if currency != wallet.currency and exchange_rate:
                calculated_amount = amount * exchange_rate

            if calculated_amount > wallet.balance:
                raise ValidationError('Hamyonda yetarli mablag\' mavjud emas')

        # Tranzaksiya vaqti hamyon yaratilgan vaqtdan oldin bo'lmasligi kerak
        transaction_created_at = cleaned_data.get('created_at')
        if wallet and transaction_created_at:
            if transaction_created_at < wallet.created_at:
                formatted_date = wallet.created_at.strftime('%d.%m.%Y %H:%M')
                raise ValidationError(f"Tranzaksiya vaqti hamyon yaratilgan vaqtdan ({formatted_date}) oldin bo'lishi mumkin emas")

        return cleaned_data



class StatisticsFilterForm(forms.Form):
    """Statistika filterlash"""

    PERIOD_CHOICES = [
        ('daily', 'Kunlik'),
        ('weekly', 'Haftalik'),
        ('monthly', 'Oylik'),
        ('yearly', 'Yillik'),
        ('custom', 'Belgilangan muddat'),
    ]

    period = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_period'
        }),
        label="Davr"
    )

    # Kunlik uchun
    day = forms.IntegerField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_day'
        }),
        label="Kun"
    )

    # Oylik uchun
    month = forms.IntegerField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_month'
        }),
        label="Oy"
    )

    # Yillik uchun
    year = forms.IntegerField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_year'
        }),
        label="Yil"
    )

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'id_start_date'
        }),
        label="Boshlanish sanasi"
    )

    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'id_end_date'
        }),
        label="Tugash sanasi"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import datetime
        import calendar

        today = datetime.now().date()
        
        # Kunlar ro'yxati (joriy oyning kunlari)
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        day_choices = [('', '--- Kun tanlang ---')]
        day_choices.extend([(i, f"{i}-kun") for i in range(1, days_in_month + 1)])
        self.fields['day'].widget.choices = day_choices
        
        # Oylar ro'yxati
        month_names = [
            'Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun',
            'Iyul', 'Avgust', 'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr'
        ]
        month_choices = [('', '--- Oy tanlang ---')]
        month_choices.extend([(i, month_names[i-1]) for i in range(1, 13)])
        self.fields['month'].widget.choices = month_choices
        
        # Yillar ro'yxati (hozirgi yildan 10 yil orqaga)
        year_choices = [('', '--- Yil tanlang ---')]
        year_choices.extend([(y, str(y)) for y in range(today.year, today.year - 11, -1)])
        self.fields['year'].widget.choices = year_choices

    def clean(self):
        cleaned_data = super().clean()
        period = cleaned_data.get('period')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if period == 'custom':
            if not start_date or not end_date:
                raise ValidationError('Belgilangan muddat uchun sanalar majburiy')

            if start_date > end_date:
                raise ValidationError('Boshlanish sanasi tugash sanasidan katta bo\'lishi mumkin emas')

        return cleaned_data