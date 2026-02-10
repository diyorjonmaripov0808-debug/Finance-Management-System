from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from functools import wraps
from .models import Transfer
from .forms import TransferForm


def user_transfer_required(view_func):
    """Foydalanuvchi o'z o'tkazmalarini boshqara oladi"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        pk = kwargs.get('pk')
        transfer = get_object_or_404(Transfer, pk=pk, is_deleted=False)
        
        # Faqat from_wallet egasi o'chira oladi
        if transfer.from_wallet.user != request.user:
            messages.error(request, 'Ruxsat yo\'q')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def transfer_list_view(request):
    """O'tkazmalar tarixi - faqat o'z o'tkazmalarini ko'rish"""
    transfers = Transfer.objects.filter(
        from_wallet__user=request.user,
        is_deleted=False
    ).select_related('from_wallet', 'to_wallet').order_by('-created_at')

    return render(request, 'transfers/list.html', {'transfers': transfers})


@login_required
def transfer_create_view(request):
    """O'tkazma yaratish"""

    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)

        if form.is_valid():
            try:
                transfer = form.save(commit=False)
                transfer.save()

                messages.success(request, 'O\'tkazma muvaffaqiyatli amalga oshirildi')
                return redirect('transfer_list')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = TransferForm(user=request.user)

    # Pass wallets data to template
    import json
    from wallets.models import Wallet
    
    wallets_data = {
        str(w.id): {
            'currency': w.currency,
            'balance': str(w.balance),
            'wallet_type': w.wallet_type,
            'card_type': w.card_type or '',
            'title': w.title or ''
        } for w in Wallet.objects.filter(user=request.user, is_deleted=False)
    }

    return render(request, 'transfers/create.html', {
        'form': form,
        'wallets_data': json.dumps(wallets_data)
    })


@login_required
@user_transfer_required
def transfer_delete_view(request, pk):
    """O'tkazma o'chirish - faqat from_wallet egasi"""
    transfer = get_object_or_404(
        Transfer,
        pk=pk,
        is_deleted=False
    )

    if request.method == 'POST':
        transfer.delete()
        messages.success(request, 'O\'tkazma bekor qilindi (pullar qaytarildi)')
        return redirect('transfer_list')

    return render(request, 'transfers/delete.html', {'transfer': transfer})