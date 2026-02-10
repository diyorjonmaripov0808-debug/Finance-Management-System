from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import uuid

from users.models import User, PhoneOTP
from users.forms import (
    PhoneNumberForm, OTPVerificationForm, AdditionalInfoForm,
    LoginForm, ProfileUpdateForm, ForgotPasswordForm, ResetPasswordForm
)


def register_step1_view(request):
    """1. Telefon raqam kiritish"""

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            
            # Check if user already exists
            user = User.objects.filter(phone_number=phone_number).first()
            
            if user:
                if user.auth_status == 'CLIENT':
                    form.add_error('phone_number', "Bu telefon raqam allaqachon ro'yxatdan o'tgan. Tizimga kiring yoki parolni tiklang.")
                    return render(request, 'users/register_step1.html', {'form': form})
                else:
                    # User exists but registration not finished, reset status and continue
                    user.auth_status = 'NEW'
                    user.save()
            else:
                # Create new user
                random_password = uuid.uuid4().hex[:10]
                user = User.objects.create(
                    phone_number=phone_number,
                    password=random_password,
                    auth_status='NEW'
                )
                user.set_password(random_password)
                user.save()

            # Create or update OTP
            otp = PhoneOTP.objects.create(user=user)

            print(f"OTP kod {phone_number} uchun: {otp.verification_code}")
            print(f"Kod {otp.code_expires_at} gacha amal qiladi (3 daqiqa)")

            request.session['register_user_id'] = str(user.id)

            messages.success(request, 'Telefoningizga kod yuborildi')
            return redirect('register_step2')
    else:
        form = PhoneNumberForm()

    return render(request, 'users/register_step1.html', {'form': form})


def register_step2_view(request):
    """2. OTP kodni tasdiqlash"""

    user_id = request.session.get('register_user_id')
    if not user_id:
        messages.error(request, 'Avval telefon raqamni kiriting')
        return redirect('register_step1')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST, user=user)

        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']

            otp = PhoneOTP.objects.get(
                user=user,
                verification_code=verification_code,
                confirmed=False,
                is_deleted=False
            )

            otp.confirmed = True
            otp.save()

            user.auth_status = 'CODE_VERIFIED'
            user.save()

            messages.success(request, 'Telefon raqam tasdiqlandi!')
            return redirect('register_step3')
    else:
        form = OTPVerificationForm(user=user)

    return render(request, 'users/register_step2.html', {
        'form': form,
        'phone_number': user.phone_number
    })


def resend_otp_view(request):
    """2.2 Qayta kod yuborish"""

    user_id = request.session.get('register_user_id')
    if not user_id:
        return redirect('register_step1')

    user = get_object_or_404(User, id=user_id)

    active_otp = PhoneOTP.objects.filter(
        user=user,
        confirmed=False,
        is_deleted=False
    ).order_by('-created_at').first()

    if active_otp and not active_otp.is_expired():
        messages.warning(request, 'Sizda hali aktiv verification_code bor')
        return redirect('register_step2')

    otp = PhoneOTP.objects.create(user=user)
    print(f"Yangi OTP kod {user.phone_number} uchun: {otp.verification_code}")

    messages.success(request, 'Yangi kod yuborildi')
    return redirect('register_step2')


def register_step3_view(request):
    """3. Qo'shimcha ma'lumotlar (ixtiyoriy)"""

    user_id = request.session.get('register_user_id')
    if not user_id:
        return redirect('register_step1')

    user = get_object_or_404(User, id=user_id)

    if user.auth_status != 'CODE_VERIFIED':
        messages.error(request, 'Avval kodni tasdiqlang')
        return redirect('register_step2')

    if request.method == 'POST':
        form = AdditionalInfoForm(request.POST, user=user)

        if form.is_valid():
            if form.cleaned_data.get('first_name'):
                user.first_name = form.cleaned_data['first_name']
            if form.cleaned_data.get('last_name'):
                user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data.get('username'):
                user.username = form.cleaned_data['username']
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])

            user.auth_status = 'CLIENT'
            user.save()

            # Automatic login
            from django.contrib.auth import login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            del request.session['register_user_id']

            messages.success(request, 'Ro\'yxatdan o\'tish muvaffaqiyatli yakunlandi! Tizimga xush kelibsiz.')
            return redirect('dashboard')
    else:
        form = AdditionalInfoForm(user=user)

    return render(request, 'users/register_step3.html', {'form': form})


def login_view(request):
    """5. Kirish"""

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(phone_number=phone_number, is_deleted=False)

                if user.check_password(password):
                    login(request, user)
                    messages.success(request, f'Xush kelibsiz, {user.first_name or user.phone_number}!')
                    if user.is_staff:
                        return redirect('admin_chat_list')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Telefon raqam yoki parol noto\'g\'ri')
            except User.DoesNotExist:
                messages.error(request, 'Telefon raqam yoki parol noto\'g\'ri')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    """4. Chiqish"""
    logout(request)
    messages.success(request, 'Tizimdan chiqdingiz')
    return redirect('login')


@login_required
def profile_update_view(request):
    """Profilni yangilash - faqat o'z profili"""
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profil muvaffaqiyatli yangilandi')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def dashboard_view(request):
    """Asosiy sahifa"""
    from wallets.models import Wallet
    from transactions.models import Transaction
    from categories.models import Category
    from django.db.models import Sum, F

    user = request.user

    wallets = Wallet.objects.filter(user=user, is_deleted=False)
    
    # Balance by currency
    balance_by_currency = {}
    for wallet in wallets:
        if wallet.currency not in balance_by_currency:
            balance_by_currency[wallet.currency] = 0
        balance_by_currency[wallet.currency] += float(wallet.balance)

    recent_transactions = Transaction.objects.filter(
        wallet__user=user,
        is_deleted=False
    ).select_related('wallet', 'category').order_by('-created_at')[:10]

    today = timezone.now().date()

    income_categories = Category.objects.filter(user=user, type='income', is_deleted=False)
    expense_categories = Category.objects.filter(user=user, type='expense', is_deleted=False)

    # Daily income by currency
    daily_income_by_currency = {}
    income_txns = Transaction.objects.filter(
        wallet__user=user,
        category__in=income_categories,
        created_at__date=today,
        is_deleted=False
    ).select_related('wallet')
    
    for txn in income_txns:
        currency = txn.wallet.currency
        converted_amount = float(txn.calculate_converted_amount())
        if currency not in daily_income_by_currency:
            daily_income_by_currency[currency] = 0
        daily_income_by_currency[currency] += converted_amount

    # Daily expense by currency
    daily_expense_by_currency = {}
    expense_txns = Transaction.objects.filter(
        wallet__user=user,
        category__in=expense_categories,
        created_at__date=today,
        is_deleted=False
    ).select_related('wallet')
    
    for txn in expense_txns:
        currency = txn.wallet.currency
        converted_amount = float(txn.calculate_converted_amount())
        if currency not in daily_expense_by_currency:
            daily_expense_by_currency[currency] = 0
        daily_expense_by_currency[currency] += converted_amount

    # Total balance (for display compatibility)
    total_balance = sum(balance_by_currency.values())

    context = {
        'wallets': wallets,
        'wallet_count': wallets.count(),
        'total_balance': total_balance,
        'balance_by_currency': balance_by_currency,
        'daily_income_by_currency': daily_income_by_currency,
        'daily_expense_by_currency': daily_expense_by_currency,
        'recent_transactions': recent_transactions,
    }

    return render(request, 'dashboard.html', context)


def forgot_password_view(request):
    """Parolni tiklash - 1. Telefon raqam kiritish"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            user = User.objects.get(phone_number=phone_number, is_deleted=False)

            # Generate OTP
            otp = PhoneOTP.objects.create(user=user)
            print(f"OTP kod {phone_number} uchun: {otp.verification_code}")

            request.session['reset_user_id'] = str(user.id)
            messages.success(request, 'Tasdiqlash kodi yuborildi')
            return redirect('forgot_password_verify')
    else:
        form = ForgotPasswordForm()

    return render(request, 'users/forgot_password.html', {'form': form})


def forgot_password_verify_view(request):
    """Parolni tiklash - 2. Kodni tasdiqlash"""
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST, user=user)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']
            otp = PhoneOTP.objects.get(
                user=user,
                verification_code=verification_code,
                confirmed=False,
                is_deleted=False
            )
            otp.confirmed = True
            otp.save()

            # Mark in session that OTP is verified
            request.session['reset_otp_verified'] = True
            return redirect('reset_password_confirm')
    else:
        form = OTPVerificationForm(user=user)

    return render(request, 'users/forgot_password_verify.html', {'form': form, 'phone_number': user.phone_number})


def reset_password_confirm_view(request):
    """Parolni tiklash - 3. Yangi parol o'rnatish"""
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')

    if not request.session.get('reset_otp_verified'):
        return redirect('forgot_password_verify')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()

            # Automatic login
            from django.contrib.auth import login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Clear session
            if 'reset_user_id' in request.session:
                del request.session['reset_user_id']
            if 'reset_otp_verified' in request.session:
                del request.session['reset_otp_verified']

            messages.success(request, 'Parolingiz muvaffaqiyatli yangilandi va tizimga kirdingiz!')
            return redirect('dashboard')
    else:
        form = ResetPasswordForm()

    return render(request, 'users/reset_password_confirm.html', {'form': form})