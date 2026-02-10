from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import User, PhoneOTP


class PhoneNumberForm(forms.Form):
    """1-qadam: Telefon raqam kiritish"""

    phone_regex = RegexValidator(
        regex=r'^\+998[0-9]{9}$',
        message="Telefon raqam formati: '+998901234567'"
    )

    phone_number = forms.CharField(
        max_length=13,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998901234567',
            'required': True
        }),
        label="Telefon raqam"
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number.startswith('+998') or len(phone_number) != 13:
            raise ValidationError('Bunday telefon raqam mavjud emas')

        # Agar bu login/register uchun bo'lsa, uni view da tekshiramiz.
        # Bu yerda faqat formatni tekshiramiz.
        # Register uchun: unique bo'lishi kerak.
        # Login uchun: mavjud bo'lishi kerak.
        # Shuning uchun bu yerdagi unique tekshiruvini olib tashlaymiz yoki view ga qarab moslaymiz.
        # Hozircha register uchun ishlatilayotganini hisobga olib, qoldiramiz.
        # LEKIN: Forgot password uchun ham shu form ishlatilishi mumkin, u holda user mavjud bo'lishi kerak.
        # Yaxshisi generic form qilib, unique tekshiruvini view darajasida qilgan ma'qul yoki alohida form.
        # Hozirgi kodda register uchun ishlatilmoqda.

        return phone_number


class OTPVerificationForm(forms.Form):
    """2-qadam: OTP tasdiqlash"""

    verification_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '123456',
            'maxlength': '6',
            'required': True,
            'style': 'font-size: 2rem; letter-spacing: 1rem;'
        }),
        label="Tasdiqlash kodi"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code')

        if not code:
            raise ValidationError('Ma\'lumot bo\'sh bo\'lishi mumkin emas')

        if not code.isdigit():
            raise ValidationError('Kod faqat raqamlardan iborat bo\'lishi kerak')

        if self.user:
            try:
                otp = PhoneOTP.objects.filter(
                    user=self.user,
                    confirmed=False,
                    is_deleted=False
                ).latest('created_at')

                if otp.is_expired():
                    raise ValidationError('Kodingizning amal qilish muddati tugagan')

                if otp.verification_code != code:
                    raise ValidationError('Verification code-ni xato kirittingiz')

            except PhoneOTP.DoesNotExist:
                raise ValidationError('Kod topilmadi')

        return code


class AdditionalInfoForm(forms.Form):
    """3-qadam: Qo'shimcha ma'lumotlar (ixtiyoriy)"""

    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ismingiz'
        }),
        label="Ism"
    )

    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Familiyangiz'
        }),
        label="Familiya"
    )

    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username (ixtiyoriy)'
        }),
        label="Username"
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parol (ixtiyoriy)'
        }),
        label="Parol"
    )

    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni tasdiqlang'
        }),
        label="Parolni tasdiqlang"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username:
            if len(username) < 3:
                raise ValidationError('Username kamida 3 ta belgidan iborat bo\'lishi kerak')

            if User.objects.filter(username=username).exclude(id=self.user.id if self.user else None).exists():
                raise ValidationError('Bu username allaqachon band')

        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password or confirm_password:
            if password != confirm_password:
                raise ValidationError('Parollar mos kelmadi')

            if len(password) < 8:
                raise ValidationError('Parol kamida 8 ta belgidan iborat bo\'lishi kerak')

        return cleaned_data


class LoginForm(forms.Form):
    """Login form"""

    phone_number = forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998901234567',
            'required': True
        }),
        label="Telefon raqam"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parol',
            'required': True
        }),
        label="Parol"
    )


class ProfileUpdateForm(forms.ModelForm):
    """Profilni yangilash formasi"""

    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Joriy parol'
        }),
        label="Joriy parol"
    )

    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yangi parol'
        }),
        label="Yangi parol"
    )

    confirm_new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yangi parolni tasdiqlang'
        }),
        label="Yangi parolni tasdiqlang"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'username': 'Username',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username and len(username) < 3:
            raise ValidationError('Username kamida 3 ta belgidan iborat bo\'lishi kerak')

        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError('Bu username allaqachon band')

        return username

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password or confirm_new_password:
            if not current_password:
                raise ValidationError('Parolni o\'zgartirish uchun joriy parolni kiriting')

            if not self.instance.check_password(current_password):
                raise ValidationError('Joriy parol noto\'g\'ri')

            if new_password != confirm_new_password:
                raise ValidationError('Yangi parollar mos kelmadi')

            if len(new_password) < 8:
                raise ValidationError('Yangi parol kamida 8 ta belgidan iborat bo\'lishi kerak')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

        return user


class ForgotPasswordForm(forms.Form):
    """Parolni tiklash uchun telefon raqam"""

    phone_regex = RegexValidator(
        regex=r'^\+998[0-9]{9}$',
        message="Telefon raqam formati: '+998901234567'"
    )

    phone_number = forms.CharField(
        max_length=13,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998901234567',
            'required': True
        }),
        label="Telefon raqam"
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number.startswith('+998') or len(phone_number) != 13:
            raise ValidationError('Bunday telefon raqam mavjud emas')

        if not User.objects.filter(phone_number=phone_number, is_deleted=False).exists():
            raise ValidationError('Bu telefon raqam bilan foydalanuvchi topilmadi')

        return phone_number


class ResetPasswordForm(forms.Form):
    """Parolni tiklash formasi"""

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        }),
        label="New Password:"
    )

    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        }),
        label="Confirm New Password:"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise ValidationError('Parollar mos kelmadi')

            if len(new_password) < 8:
                raise ValidationError('Parol kamida 8 ta belgidan iborat bo\'lishi kerak')

        return cleaned_data