import uuid
from django.db import models, transaction as db_transaction
from django.utils import timezone
from django.core.validators import MinValueValidator
from users.models import BaseModel, User
from wallets.models import Wallet
from categories.models import Category


class Transaction(BaseModel):
    class Currency(models.TextChoices):
        UZS = 'UZS', 'UZS'
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'
        RUB = 'Rub', 'RUB'

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0.01)])
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Tranzaksiya"
        verbose_name_plural = "Tranzaksiyalar"
        ordering = ['-created_at']

    def calculate_converted_amount(self):
        """Valyuta konvertatsiya bilan hisoblanadi"""
        if self.currency == self.wallet.currency:
            return self.amount
        elif self.exchange_rate:
            return self.amount * self.exchange_rate
        else:
            # Agar valyuta kursi bo'lmasa, asl miqdorni qaytarish
            return self.amount

    def calculate_wallet_amount(self):
        """Hamyonga tegishli miqdorni hisoblaydi"""
        return self.calculate_converted_amount()

    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.category.type == 'expense':
            # Balance check needs to consider exchange rate
            try:
                converted_amount = self.calculate_converted_amount()
                if converted_amount > self.wallet.balance:
                    raise ValidationError({'amount': 'Hisobda yetarli mablag\' mavjud emas'})
            except ValidationError as e:
                # If calculate_converted_amount fails, it means exchange rate is missing
                # But we might want to attach error to exchange_rate field
                if "Valyuta kursi" in str(e):
                    raise ValidationError({'exchange_rate': 'Valyuta kursi kiritilishi shart'})
                raise e

    def save(self, *args, **kwargs):
        # Check if this is a new object being created (not just pk being None)
        is_new = self._state.adding
        
        self.clean()
        
        # Only update balance on creation
        if is_new:
            from django.db import transaction
            with transaction.atomic():
                self.wallet.refresh_from_db()
                
                if self.category.type == 'income':
                    converted_amount = self.calculate_converted_amount()
                    self.wallet.balance += converted_amount
                    self.wallet.save()
                elif self.category.type == 'expense':
                    converted_amount = self.calculate_converted_amount()
                    # Final safety check before deducting
                    if self.wallet.balance < converted_amount:
                        raise ValueError("Balans yetarli emas")
                    self.wallet.balance -= converted_amount
                    self.wallet.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Reverse transaction on delete
        if not self.is_deleted:
            if self.category.type == 'income':
                converted_amount = self.calculate_converted_amount()
                self.wallet.balance -= converted_amount
            elif self.category.type == 'expense':
                converted_amount = self.calculate_converted_amount()
                self.wallet.balance += converted_amount

            self.wallet.save()
            self.is_deleted = True
            self.save()

    def __str__(self):
        return f"{self.category.name} - {self.amount} {self.currency}"