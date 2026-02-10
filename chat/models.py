from django.db import models
from django.utils.translation import gettext_lazy as _
from base.models import BaseModel
from users.models import User


class Conversation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='admin_conversations',
        limit_choices_to={'is_staff': True}
    )

    class Meta:
        verbose_name = _("Suhbat")
        verbose_name_plural = _("Suhbatlar")
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.phone_number} - {self.admin.username}"

    def get_unread_count(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(BaseModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField(verbose_name=_("Xabar matni"))
    is_read = models.BooleanField(default=False, verbose_name=_("O'qilgan"))

    class Meta:
        verbose_name = _("Xabar")
        verbose_name_plural = _("Xabarlar")
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.phone_number}: {self.text[:50]}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Foydalanuvchi faolligini yangilash
        self.sender.save(update_fields=['updated_at'])
        # Suhbat vaqtini yangilash (dashboard-da sorting uchun)
        self.conversation.save()