from django.db import models
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    """Umumiy asosiy model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    is_deleted = models.BooleanField(default=False, verbose_name="O'chirilgan")

    class Meta:
        abstract = True
        ordering = ['-created_at']