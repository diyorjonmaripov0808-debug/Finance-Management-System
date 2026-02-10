from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid
import random
import string
from base.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Telefon raqam kiritilishi shart')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('auth_status', 'CLIENT')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser, BaseModel):
    AUTH_STATUS = (
        ('NEW', 'Yangi'),
        ('CODE_VERIFIED', 'Kod tasdiqlangan'),
        ('CLIENT', 'Mijoz'),
    )

    phone_regex = RegexValidator(
        regex=r'^\+998[0-9]{9}$',
        message="Telefon raqam formati: '+998901234567'"
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[phone_regex],
        unique=True,
        verbose_name="Telefon raqam"
    )

    auth_status = models.CharField(
        max_length=20,
        choices=AUTH_STATUS,
        default='NEW',
        verbose_name="Holat"
    )

    first_name = models.CharField(max_length=100, blank=True, verbose_name="Ism")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Familiya")

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"user_{uuid.uuid4().hex[:10]}"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} {self.last_name}"
        return self.phone_number


class PhoneOTP(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    verification_code = models.CharField(max_length=6, verbose_name="Tasdiqlash kodi")
    confirmed = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    code_expires_at = models.DateTimeField(verbose_name="Kod amal qilish muddati")

    class Meta:
        verbose_name = "OTP kod"
        verbose_name_plural = "OTP kodlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.phone_number} - {self.verification_code}"

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k=6))

    def is_expired(self):
        return timezone.now() > self.code_expires_at

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = self.generate_code()
        if not self.code_expires_at:
            self.code_expires_at = timezone.now() + timezone.timedelta(minutes=3)
        super().save(*args, **kwargs)