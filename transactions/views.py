from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.db import transaction as db_transaction
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from functools import wraps
import json

from .models import Transaction
from .forms import IncomeForm, ExpenseForm, StatisticsFilterForm
from wallets.models import Wallet
from categories.models import Category


def user_transaction_required(view_func):
    """Foydalanuvchi o'z tranzaksiyalarini boshqara oladi"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        pk = kwargs.get('pk')
        transaction = get_object_or_404(Transaction, pk=pk, is_deleted=False)
        
        if transaction.wallet.user != request.user:
            messages.error(request, 'Ruxsat yo\'q')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def transaction_list_view(request):
    # Apply filters from GET params
    """Tranzaksiyalar ro'yxati - faqat o'z tranzaksiyalari"""
    transactions = Transaction.objects.filter(
        wallet__user=request.user,
        is_deleted=False
    ).select_related('wallet', 'category').order_by('-created_at')

    wallet_id = request.GET.get('wallet')
    category_id = request.GET.get('category')
    t_type = request.GET.get('type')
    date = request.GET.get('date')

    if wallet_id:
        transactions = transactions.filter(wallet_id=wallet_id)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if t_type in ('income', 'expense'):
        transactions = transactions.filter(category__type=t_type)
    if date:
        transactions = transactions.filter(created_at__date=date)

    # Provide wallets and categories for filter selects
    wallets = Wallet.objects.filter(user=request.user, is_deleted=False)
    categories = Category.objects.filter(user=request.user, is_deleted=False)

    context = {
        'transactions': transactions,
        'wallets': wallets,
        'categories': categories,
        'filters': {
            'wallet': wallet_id,
            'category': category_id,
            'type': t_type,
            'date': date,
        }
    }

    return render(request, 'transactions/list.html', context)

@login_required
@db_transaction.atomic
def income_create_view(request):
    """Kirim qo'shish"""

    if request.method == 'POST':
        form = IncomeForm(request.POST, user=request.user)

        if form.is_valid():
            transaction = form.save(commit=False)
            # Ensure wallet is set correctly
            transaction.wallet = form.cleaned_data['wallet']
            transaction.save()

            messages.success(request, 'Kirim qo\'shildi')
            return redirect('transaction_list')
    else:
        form = IncomeForm(user=request.user)

    # Get all user wallets
    user_wallets = Wallet.objects.filter(user=request.user, is_deleted=False)
    
    wallets_data = {}
    for w in user_wallets:
        wallets_data[str(w.id)] = {
            'currency': w.currency,
            'balance': str(w.balance),
            'wallet_type': w.wallet_type,
            'card_type': w.card_type or '',
            'title': w.title or ''
        }
    
    return render(request, 'transactions/income_create.html', {
        'form': form,
        'wallets_data': json.dumps(wallets_data),
        'has_wallets': user_wallets.exists()
    })


@login_required
@db_transaction.atomic
def expense_create_view(request):
    """Chiqim qo'shish"""

    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)

        if form.is_valid():
            transaction = form.save(commit=False)
            # Ensure wallet is set correctly
            transaction.wallet = form.cleaned_data['wallet']
            transaction.save()

            messages.success(request, 'Chiqim qo\'shildi')
            return redirect('transaction_list')
    else:
        form = ExpenseForm(user=request.user)

    # Get all user wallets
    user_wallets = Wallet.objects.filter(user=request.user, is_deleted=False)
    
    wallets_data = {}
    for w in user_wallets:
        wallets_data[str(w.id)] = {
            'currency': w.currency,
            'balance': str(w.balance),
            'wallet_type': w.wallet_type,
            'card_type': w.card_type or '',
            'title': w.title or ''
        }
    
    return render(request, 'transactions/expense_create.html', {
        'form': form,
        'wallets_data': json.dumps(wallets_data),
        'has_wallets': user_wallets.exists()
    })


@login_required
@user_transaction_required
def transaction_delete_view(request, pk):
    """Tranzaksiya o'chirish - faqat egasi"""
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        is_deleted=False
    )

    if request.method == 'POST':
        wallet = transaction.wallet
        try:
            calculated_amount = transaction.calculate_wallet_amount()
        except Exception:
            calculated_amount = transaction.amount

        if transaction.category.type == 'income':
            wallet.balance -= calculated_amount
        else:
            wallet.balance += calculated_amount
        wallet.save()

        transaction.is_deleted = True
        transaction.save()

        messages.success(request, 'Tranzaksiya o\'chirildi')
        return redirect('transaction_list')

    return render(request, 'transactions/delete.html', {'transaction': transaction})


@login_required
def statistics_view(request):
    """Statistika - kunlik, haftalik, oylik, yillik"""

    period = request.GET.get('period', 'monthly')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Dropdown qiymatlari
    selected_day = request.GET.get('day')
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    today = datetime.now().date()

    if period == 'daily':
        # Kunlik: Agar kun tanlangan bo'lsa, o'sha kunning statistikasi
        if selected_day:
            try:
                day_num = int(selected_day)
                date_from = today.replace(day=day_num)
                date_to = date_from
            except (ValueError, TypeError):
                # Agar kun noto'g'ri bo'lsa, bugungi kunni ishlatamiz
                date_from = today
                date_to = today
        else:
            # Agar kun tanlanmagan bo'lsa, bugungi kun
            date_from = today
            date_to = today
    elif period == 'weekly':
        # Haftalik: Joriy hafta (Dushanba - Yakshanba)
        weekday = today.weekday()  # 0 = Monday, 6 = Sunday
        date_from = today - timedelta(days=weekday)
        date_to = date_from + timedelta(days=6)
    elif period == 'monthly':
        # Oylik: Agar oy tanlangan bo'lsa, o'sha oyning statistikasi
        if selected_month:
            try:
                month_num = int(selected_month)
                # Tanlangan oyning birinchi kuni
                date_from = today.replace(month=month_num, day=1)
                # Tanlangan oyning oxirgi kuni
                import calendar
                last_day = calendar.monthrange(today.year, month_num)[1]
                date_to = today.replace(month=month_num, day=last_day)
            except (ValueError, TypeError):
                # Agar oy noto'g'ri bo'lsa, joriy oyni ishlatamiz
                date_from = today.replace(day=1)
                date_to = today
        else:
            # Agar oy tanlanmagan bo'lsa, joriy oy
            date_from = today.replace(day=1)
            date_to = today
    elif period == 'yearly':
        # Yillik: Agar yil tanlangan bo'lsa, o'sha yilning statistikasi
        if selected_year:
            try:
                year_num = int(selected_year)
                # Tanlangan yilning 1-yanvari
                date_from = today.replace(year=year_num, month=1, day=1)
                # Tanlangan yilning 31-dekabri
                date_to = today.replace(year=year_num, month=12, day=31)
            except (ValueError, TypeError):
                # Agar yil noto'g'ri bo'lsa, joriy yilni ishlatamiz
                date_from = today.replace(month=1, day=1)
                date_to = today
        else:
            # Agar yil tanlanmagan bo'lsa, joriy yil
            date_from = today.replace(month=1, day=1)
            date_to = today
    elif period == 'custom' and start_date and end_date:
        try:
            date_from = datetime.strptime(start_date, '%Y-%m-%d').date()
            date_to = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            # Agar sana formati noto'g'ri bo'lsa, default qiymatni ishlatamiz
            date_from = today.replace(day=1)
            date_to = today
    else:
        # Default: joriy oy
        date_from = today.replace(day=1)
        date_to = today

    income_categories = Category.objects.filter(
        user=request.user,
        type='income',
        is_deleted=False
    )

    expense_categories = Category.objects.filter(
        user=request.user,
        type='expense',
        is_deleted=False
    )

    income_transactions = Transaction.objects.filter(
        wallet__user=request.user,
        category__in=income_categories,
        created_at__date__gte=date_from,
        created_at__date__lte=date_to,
        is_deleted=False
    )

    expense_transactions = Transaction.objects.filter(
        wallet__user=request.user,
        category__in=expense_categories,
        created_at__date__gte=date_from,
        created_at__date__lte=date_to,
        is_deleted=False
    )

    # Totals per currency (use original transaction currency for grouping)
    from collections import defaultdict
    from decimal import Decimal

    totals_by_currency = defaultdict(lambda: {
        'total_income': Decimal('0.00'),
        'total_expense': Decimal('0.00'),
        'income_by_category': {},
        'expense_by_category': {}
    })

    # Sum income transactions per currency and category
    for trans in income_transactions:
        cur = trans.currency or 'UZS'
        try:
            amt = Decimal(str(trans.amount))
        except Exception:
            amt = Decimal('0.00')

        totals_by_currency[cur]['total_income'] += amt
        cat = trans.category.name
        totals_by_currency[cur]['income_by_category'][cat] = (
            totals_by_currency[cur]['income_by_category'].get(cat, Decimal('0.00')) + amt
        )

    # Sum expense transactions per currency and category
    for trans in expense_transactions:
        cur = trans.currency or 'UZS'
        try:
            amt = Decimal(str(trans.amount))
        except Exception:
            amt = Decimal('0.00')

        totals_by_currency[cur]['total_expense'] += amt
        cat = trans.category.name
        totals_by_currency[cur]['expense_by_category'][cat] = (
            totals_by_currency[cur]['expense_by_category'].get(cat, Decimal('0.00')) + amt
        )

    # Compute overall totals (converted to wallet amounts if needed previously)
    total_income = sum([v['total_income'] for v in totals_by_currency.values()])
    total_expense = sum([v['total_expense'] for v in totals_by_currency.values()])
    income_by_category = {}
    for trans in income_transactions:
        try:
            cat_name = trans.category.name
            amount = trans.calculate_wallet_amount()
            income_by_category[cat_name] = income_by_category.get(cat_name, 0) + amount
        except Exception:
            cat_name = trans.category.name
            income_by_category[cat_name] = income_by_category.get(cat_name, 0) + trans.amount

    expense_by_category = {}
    for trans in expense_transactions:
        try:
            cat_name = trans.category.name
            amount = trans.calculate_wallet_amount()
            expense_by_category[cat_name] = expense_by_category.get(cat_name, 0) + amount
        except Exception:
            cat_name = trans.category.name
            expense_by_category[cat_name] = expense_by_category.get(cat_name, 0) + trans.amount

    # Init form
    form = StatisticsFilterForm(request.GET or None)
    
    if form.is_valid():
        if period == 'custom':
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            if start_date and end_date:
                date_from = start_date
                date_to = end_date

    period_names = {
        'daily': 'Kunlik',
        'weekly': 'Haftalik',
        'monthly': 'Oylik',
        'yearly': 'Yillik',
        'custom': 'Belgilangan muddat'
    }
    period_name = period_names.get(period, 'Oylik')

    context = {
        'form': form,
        'period': period,
        'period_name': period_name,
        'date_from': date_from,
        'date_to': date_to,
        'total_income': total_income,
        'total_expense': total_expense,
        'income_by_category': income_by_category,
        'expense_by_category': expense_by_category,
        'income_transactions': income_transactions,
        'expense_transactions': expense_transactions,
        'totals_by_currency': dict(totals_by_currency),
    }

    return render(request, 'transactions/statistics.html', context)


