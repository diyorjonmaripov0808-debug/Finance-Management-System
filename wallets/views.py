from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wallet
from .forms import WalletForm


def wallet_owner_required(view_func):
    """Hamyon egasi bo'lishini tekshiri"""
    def wrapper(request, *args, **kwargs):
        pk = kwargs.get('pk')
        wallet = get_object_or_404(Wallet, pk=pk, is_deleted=False)
        
        if wallet.user != request.user:
            messages.error(request, 'Ruxsat yo\'q')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def wallet_list_view(request):
    """Hamyonlar ro'yxati - faqat o'z hamyonlari"""
    wallets = Wallet.objects.filter(user=request.user, is_deleted=False)

    # Compute totals grouped by currency
    balance_by_currency = {}
    for wallet in wallets:
        balance_by_currency.setdefault(wallet.currency, 0)
        balance_by_currency[wallet.currency] += float(wallet.balance)

    context = {
        'wallets': wallets,
        'balance_by_currency': balance_by_currency,
        'wallet_count': wallets.count(),
    }

    return render(request, 'wallets/list.html', context)


@login_required
def wallet_create_view(request):
    if request.method == 'POST':
        form = WalletForm(
            request.POST,
            initial={'user': request.user}
        )

        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()

            messages.success(request, 'Hamyon yaratildi')
            return redirect('wallet_list')
    else:
        form = WalletForm(initial={'user': request.user})

    return render(request, 'wallets/create.html', {'form': form})



@login_required
@wallet_owner_required
def wallet_update_view(request, pk):
    """Hamyon tahrirlash - faqat egasi"""
    wallet = get_object_or_404(Wallet, pk=pk, is_deleted=False)

    if request.method == 'POST':
        form = WalletForm(request.POST, instance=wallet)

        if form.is_valid():
            form.save()
            messages.success(request, 'Hamyon yangilandi')
            return redirect('wallet_list')
    else:
        form = WalletForm(instance=wallet)

    return render(request, 'wallets/update.html', {'form': form, 'wallet': wallet})


@login_required
@wallet_owner_required
def wallet_delete_view(request, pk):
    """Hamyon o'chirish - faqat egasi"""
    wallet = get_object_or_404(Wallet, pk=pk, is_deleted=False)

    if request.method == 'POST':
        wallet.is_deleted = True
        wallet.save()
        messages.success(request, 'Hamyon o\'chirildi')
        return redirect('wallet_list')

    return render(request, 'wallets/delete.html', {'wallet': wallet})