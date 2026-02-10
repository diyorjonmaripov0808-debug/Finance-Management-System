from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from base.models import BaseModel
from users.models import User


class Wallet(BaseModel):
    WALLET_TYPES = (
        ('naqd', 'Naqd pul'),
        ('karta', 'Bank kartasi'),
    )

    CARD_TYPES = (
        ('HUMO', 'Humo'),
        ('UZCARD', 'Uzcard'),
        ('VISA', 'Visa'),
        ('MASTERCARD', 'Mastercard'),
    )

    CURRENCIES = (
        ('UZS', 'So\'m'),
        ('USD', 'Dollar'),
        ('EUR', 'Evro'),
        ('RUB', 'Rubl'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    wallet_type = models.CharField(max_length=10, choices=WALLET_TYPES, default='naqd')
    card_type = models.CharField(max_length=20, choices=CARD_TYPES, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nomi")
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='UZS')
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Hamyon"
        verbose_name_plural = "Hamyonlar"
        ordering = ['-created_at']

        constraints = [
            # NAQD
            models.UniqueConstraint(
                fields=['user', 'wallet_type', 'currency'],
                condition=Q(wallet_type='naqd', is_deleted=False),
                name='unique_naqd_wallet_per_currency'
            ),
            # KARTA
            models.UniqueConstraint(
                fields=['user', 'wallet_type', 'card_type', 'title', 'currency'],
                condition=Q(wallet_type='karta', is_deleted=False),
                name='unique_card_wallet'
            ),
        ]

    def clean(self):
        if self.wallet_type == 'karta':
            if not self.card_type:
                raise ValidationError({'card_type': 'Karta turini tanlang'})
            if not self.title:
                raise ValidationError({'title': 'Karta nomini kiriting'})
        elif self.wallet_type == 'naqd':
            self.card_type = None
            self.title = None

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        # Avoid including the live balance in the default string representation
        # to prevent accidental rendering of balances in templates.
        title = self.title or self.get_wallet_type_display()
        card = f" ({self.card_type})" if getattr(self, 'card_type', None) else ""
        return f"{title}{card} ({self.currency})"