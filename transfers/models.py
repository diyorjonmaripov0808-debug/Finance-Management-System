# transfers/models.py
from django.db import models, transaction as db_transaction
from base.models import BaseModel
from wallets.models import Wallet
from decimal import Decimal


class Transfer(BaseModel):
    from_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transfers_from',
        verbose_name="Qaysi hamyondan"
    )
    to_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transfers_to',
        verbose_name="Qaysi hamyonga"
    )

    from_amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Miqdor")
    to_amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Olinadigan miqdor")

    exchange_rate = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        null=True,
        blank=True,
        verbose_name="Kurs"
    )

    class Meta:
        verbose_name = "O'tkazma"
        verbose_name_plural = "O'tkazmalar"
        ordering = ['-created_at']

    def __str__(self):
        from_user = self.from_wallet.user.phone_number if self.from_wallet.user else "Unknown"
        to_user = self.to_wallet.user.phone_number if self.to_wallet.user else "Unknown"
        return f"{from_user} → {to_user}: {self.from_amount} {self.from_wallet.currency}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.from_wallet == self.to_wallet:
            raise ValidationError({'to_wallet': 'O\'z-o\'ziga o\'tkazma qilib bo\'lmaydi'})

        if self.from_amount > self.from_wallet.balance:
            raise ValidationError({'from_amount': 'Hisobda yetarli mablag\' mavjud emas'})

        if self.from_wallet.currency != self.to_wallet.currency and not self.exchange_rate:
             raise ValidationError({'exchange_rate': 'Valyutalar har xil bo\'lganda kurs kiritilishi shart'})

    def save(self, *args, **kwargs):
        self.clean()
        is_new = self._state.adding

        # Hisoblash to_amount
        if self.from_wallet.currency == self.to_wallet.currency:
            self.to_amount = self.from_amount
            self.exchange_rate = None
        elif self.exchange_rate:
            self.to_amount = self.from_amount * self.exchange_rate
        else:
            self.to_amount = self.from_amount

        super().save(*args, **kwargs)

        if is_new:
            # Balansni yangilash - atomic transaction
            from django.db import transaction
            with transaction.atomic():
                # Refresh current balances
                self.from_wallet.refresh_from_db()
                self.to_wallet.refresh_from_db()
                
                # Final safety check - balance should not go negative
                if self.from_wallet.balance < self.from_amount:
                    raise ValueError("Balans yetarli emas - transfer amalga oshirilmadi")
                
                self.from_wallet.balance -= self.from_amount
                self.from_wallet.save()

                self.to_wallet.balance += self.to_amount
                self.to_wallet.save()

    def delete(self, *args, **kwargs):
        if not self.is_deleted:
            # Reverse balances
            self.from_wallet.refresh_from_db()
            self.to_wallet.refresh_from_db()

            self.from_wallet.balance += self.from_amount
            self.to_wallet.balance -= self.to_amount
            
            self.from_wallet.save()
            self.to_wallet.save()

            self.is_deleted = True
            self.save()