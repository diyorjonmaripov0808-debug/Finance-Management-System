# base/templatetags/finance_filters.py
from django import template
from django.db.models import Sum, Q
from decimal import Decimal

register = template.Library()


@register.filter
def dictsum(value, key):
    """
    Dictionary yoki queryset'dan berilgan kalit bo'yicha yig'indini hisoblash.
    Misol: {{ wallets|dictsum:"balance" }}
    """
    if hasattr(value, 'aggregate'):
        # Agar queryset bo'lsa
        result = value.aggregate(sum=Sum(key))['sum']
        return result if result else Decimal('0.00')

    elif hasattr(value, '__iter__'):
        # Agar list yoki queryset bo'lsa
        total = Decimal('0.00')
        for item in value:
            if hasattr(item, key):
                val = getattr(item, key, 0)
                total += Decimal(str(val)) if val else Decimal('0.00')
            elif isinstance(item, dict):
                val = item.get(key, 0)
                total += Decimal(str(val)) if val else Decimal('0.00')
        return total

    return Decimal('0.00')


@register.filter
def income_total(transactions):
    """
    Faqat income (kirim) tranzaksiyalarining summasini hisoblash.
    Misol: {{ transactions|income_total }}
    """
    if hasattr(transactions, 'filter'):
        # Agar queryset bo'lsa
        return transactions.filter(category__type='income').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')

    # Agar list bo'lsa
    total = Decimal('0.00')
    for transaction in transactions:
        if hasattr(transaction, 'category'):
            if transaction.category.type == 'income':
                total += Decimal(str(transaction.amount))
        elif transaction.get('category_type') == 'income':
            total += Decimal(str(transaction.get('amount', 0)))

    return total


@register.filter
def expense_total(transactions):
    """
    Faqat expense (chiqim) tranzaksiyalarining summasini hisoblash.
    Misol: {{ transactions|expense_total }}
    """
    if hasattr(transactions, 'filter'):
        # Agar queryset bo'lsa
        return transactions.filter(category__type='expense').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')

    # Agar list bo'lsa
    total = Decimal('0.00')
    for transaction in transactions:
        if hasattr(transaction, 'category'):
            if transaction.category.type == 'expense':
                total += Decimal(str(transaction.amount))
        elif transaction.get('category_type') == 'expense':
            total += Decimal(str(transaction.get('amount', 0)))

    return total


@register.simple_tag
def totals_by_currency(transactions):
    """
    Return totals per currency for given transactions.
    Usage: {% totals_by_currency transactions as totals %}
    Result is a dict: { 'UZS': {'income': Decimal, 'expense': Decimal}, ... }
    """
    totals = {}
    for t in transactions:
        try:
            cur = getattr(t, 'currency', None) or 'UZS'
            if cur not in totals:
                totals[cur] = {'income': Decimal('0.00'), 'expense': Decimal('0.00')}

            # Determine type (if category present)
            if hasattr(t, 'category') and getattr(t.category, 'type', None) == 'income':
                totals[cur]['income'] += Decimal(str(getattr(t, 'amount', 0)))
            else:
                totals[cur]['expense'] += Decimal(str(getattr(t, 'amount', 0)))
        except Exception:
            # ignore problematic items
            continue

    return totals


@register.simple_tag
def transfer_totals_by_currency(transfers):
    """
    Compute sent/received totals grouped by currency for Transfer queryset/list.
    Returns dict: { 'UZS': {'sent': Decimal, 'received': Decimal}, ... }
    """
    result = {}
    for t in transfers:
        try:
            # sent
            from_cur = getattr(t.from_wallet, 'currency', 'UZS')
            to_cur = getattr(t.to_wallet, 'currency', 'UZS')

            if from_cur not in result:
                result[from_cur] = {'sent': Decimal('0.00'), 'received': Decimal('0.00')}
            if to_cur not in result:
                result[to_cur] = {'sent': Decimal('0.00'), 'received': Decimal('0.00')}

            result[from_cur]['sent'] += Decimal(str(getattr(t, 'from_amount', 0)))
            result[to_cur]['received'] += Decimal(str(getattr(t, 'to_amount', 0)))
        except Exception:
            continue

    return result


@register.filter
def sent_total(transfers):
    """
    Yuborilgan o'tkazmalarning umumiy summasini hisoblash.
    Misol: {{ transfers|sent_total }}
    """
    if hasattr(transfers, 'aggregate'):
        # Agar queryset bo'lsa
        return transfers.aggregate(
            total=Sum('from_amount')
        )['total'] or Decimal('0.00')

    # Agar list bo'lsa
    total = Decimal('0.00')
    for transfer in transfers:
        if hasattr(transfer, 'from_amount'):
            total += Decimal(str(transfer.from_amount))
        elif isinstance(transfer, dict):
            total += Decimal(str(transfer.get('from_amount', 0)))

    return total


@register.filter
def received_total(transfers):
    """
    Qabul qilingan o'tkazmalarning umumiy summasini hisoblash.
    Misol: {{ transfers|received_total }}
    """
    if hasattr(transfers, 'aggregate'):
        # Agar queryset bo'lsa
        return transfers.aggregate(
            total=Sum('to_amount')
        )['total'] or Decimal('0.00')

    # Agar list bo'lsa
    total = Decimal('0.00')
    for transfer in transfers:
        if hasattr(transfer, 'to_amount'):
            total += Decimal(str(transfer.to_amount))
        elif isinstance(transfer, dict):
            total += Decimal(str(transfer.get('to_amount', 0)))

    return total


@register.filter
def multiply(value, arg):
    """
    Ikki sonni ko'paytirish.
    Misol: {{ amount|multiply:exchange_rate }}
    """
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return Decimal('0.00')


@register.filter
def divide(value, arg):
    """
    Ikki sonni bo'lish.
    Misol: {{ total|divide:count }}
    """
    try:
        arg_decimal = Decimal(str(arg))
        if arg_decimal == 0:
            return Decimal('0.00')
        return Decimal(str(value)) / arg_decimal
    except (ValueError, TypeError):
        return Decimal('0.00')


@register.filter
def percentage(value, total):
    """
    Foizni hisoblash.
    Misol: {{ amount|percentage:total }}%
    """
    try:
        if total == 0:
            return Decimal('0.00')
        return (Decimal(str(value)) / Decimal(str(total))) * 100
    except (ValueError, TypeError):
        return Decimal('0.00')


@register.filter
def format_currency(value, currency='UZS'):
    """
    Valyuta bilan formatlash.
    Misol: {{ amount|format_currency:"USD" }}
    """
    try:
        value_decimal = Decimal(str(value))
        if currency == 'USD':
            return f"${value_decimal:,.2f}"
        elif currency == 'EUR':
            return f"€{value_decimal:,.2f}"
        elif currency == 'RUB':
            return f"{value_decimal:,.2f} ₽"
        else:  # UZS
            return f"{value_decimal:,.0f} so'm"
    except (ValueError, TypeError):
        return "0.00"


@register.filter
def wallet_balance_color(value):
    """
    Balansga qarab rang berish.
    Misol: <div class="{{ wallet.balance|wallet_balance_color }}">
    """
    try:
        balance = Decimal(str(value))
        if balance > 1000000:  # 1 million dan ko'p
            return "text-success"
        elif balance > 100000:  # 100 ming dan ko'p
            return "text-primary"
        elif balance > 0:
            return "text-warning"
        else:
            return "text-danger"
    except (ValueError, TypeError):
        return "text-secondary"


@register.filter
def transaction_type_badge(value):
    """
    Tranzaksiya turiga qarab badge class berish.
    Misol: <span class="{{ transaction.category.type|transaction_type_badge }}">
    """
    if value == 'income':
        return "badge-income"
    elif value == 'expense':
        return "badge-expense"
    return "badge-secondary"


@register.filter
def wallet_type_icon(value):
    """
    Hamyon turiga qarab icon berish.
    Misol: <i class="{{ wallet.wallet_type|wallet_type_icon }}">
    """
    if value == 'karta':
        return "fas fa-credit-card"
    elif value == 'naqd':
        return "fas fa-money-bill"
    return "fas fa-wallet"


@register.filter
def wallet_summary(wallet):
    """
    Qisqacha hamyon malumoti:
    - Naqd: "Naqd (CURRENCY)"
    - Karta: "Title (CARD_TYPE) (CURRENCY)"
    """
    if not wallet:
        return ""

    try:
        w_type = getattr(wallet, 'wallet_type', '')
        currency = getattr(wallet, 'currency', '')

        if w_type == 'naqd':
            return f"Naqd ({currency})"

        if w_type == 'karta':
            title = getattr(wallet, 'title', '') or wallet.get_wallet_type_display()
            card = getattr(wallet, 'card_type', '') or ''
            if card:
                return f"{title} ({card}) ({currency})"
            return f"{title} ({currency})"

        # Fallback
        return f"{wallet.get_wallet_type_display()} ({currency})"
    except Exception:
        return ""


@register.filter
def truncate_chars(value, max_length):
    """
    Matnni kesish.
    Misol: {{ description|truncate_chars:50 }}
    """
    if len(value) <= max_length:
        return value
    return value[:max_length] + "..."


@register.filter
def time_since(value):
    """
    Vaqtni "3 kun oldin" formatida ko'rsatish.
    Misol: {{ message.created_at|time_since }}
    """
    from django.utils import timezone
    from datetime import datetime

    if not value:
        return ""

    now = timezone.now()
    diff = now - value

    if diff.days > 365:
        years = diff.days // 365
        return f"{years} yil oldin"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} oy oldin"
    elif diff.days > 7:
        weeks = diff.days // 7
        return f"{weeks} hafta oldin"
    elif diff.days > 0:
        return f"{diff.days} kun oldin"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} soat oldin"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} daqiqa oldin"
    else:
        return "hozirgina"


@register.filter
def format_date(value, format_type='short'):
    """
    Sana va vaqtni formatlash.
    Misol: {{ created_at|format_date:"long" }}
    """
    if not value:
        return ""

    if format_type == 'long':
        return value.strftime("%d.%m.%Y %H:%M")
    elif format_type == 'date':
        return value.strftime("%d.%m.%Y")
    elif format_type == 'time':
        return value.strftime("%H:%M")
    else:  # short
        return value.strftime("%d.%m.%y")


@register.simple_tag
def calculate_balance(wallet, transactions):
    """
    Hamyon balansini tranzaksiyalar asosida hisoblash.
    {% calculate_balance wallet transactions as balance %}
    """
    from decimal import Decimal
    balance = Decimal('0.00')

    for transaction in transactions:
        if transaction.wallet_id == wallet.id:
            if transaction.category.type == 'income':
                balance += transaction.amount
            else:
                balance -= transaction.amount

    return balance


@register.simple_tag
def get_statistics(user, period='monthly'):
    """
    Statistika ma'lumotlarini olish.
    {% get_statistics user "monthly" as stats %}
    """
    from django.utils import timezone
    from datetime import datetime, timedelta
    from transactions.models import Transaction
    from categories.models import Category

    today = datetime.now().date()

    if period == 'daily':
        date_from = today
        date_to = today
    elif period == 'weekly':
        date_from = today - timedelta(days=7)
        date_to = today
    elif period == 'monthly':
        date_from = today - timedelta(days=30)
        date_to = today
    elif period == 'yearly':
        date_from = today - timedelta(days=365)
        date_to = today
    else:
        date_from = today - timedelta(days=30)
        date_to = today

    income_categories = Category.objects.filter(
        user=user,
        type='income',
        is_deleted=False
    )

    expense_categories = Category.objects.filter(
        user=user,
        type='expense',
        is_deleted=False
    )

    income_transactions = Transaction.objects.filter(
        wallet__user=user,
        category__in=income_categories,
        created_at__date__gte=date_from,
        created_at__date__lte=date_to,
        is_deleted=False
    )

    expense_transactions = Transaction.objects.filter(
        wallet__user=user,
        category__in=expense_categories,
        created_at__date__gte=date_from,
        created_at__date__lte=date_to,
        is_deleted=False
    )

    total_income = sum(t.calculate_wallet_amount() for t in income_transactions)
    total_expense = sum(t.calculate_wallet_amount() for t in expense_transactions)

    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'income_count': income_transactions.count(),
        'expense_count': expense_transactions.count(),
        'date_from': date_from,
        'date_to': date_to
    }