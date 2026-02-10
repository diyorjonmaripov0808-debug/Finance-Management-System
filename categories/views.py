from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps
from .models import Category
from .forms import CategoryForm


def user_category_required(view_func):
    """Foydalanuvchi o'z kategoriyalarini boshqara oladi"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        pk = kwargs.get('pk')
        category = get_object_or_404(Category, pk=pk, is_deleted=False)
        
        if category.user != request.user:
            messages.error(request, 'Ruxsat yo\'q')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def category_list_view(request):
    """Kategoriyalar ro'yxati - faqat o'z kategoriyalari"""
    categories = Category.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'categories/list.html', {'categories': categories})


@login_required
def category_create_view(request):
    """Kategoriya yaratish"""

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()

            messages.success(request, 'Kategoriya yaratildi')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'categories/create.html', {'form': form})


@login_required
@user_category_required
def category_update_view(request, pk):
    """Kategoriya tahrirlash - faqat egasi"""
    category = get_object_or_404(Category, pk=pk, is_deleted=False)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, 'Kategoriya yangilandi')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'categories/update.html', {'form': form, 'category': category})


@login_required
@user_category_required
def category_delete_view(request, pk):
    """Kategoriya o'chirish - faqat egasi"""
    category = get_object_or_404(Category, pk=pk, is_deleted=False)

    if request.method == 'POST':
        category.is_deleted = True
        category.save()
        messages.success(request, 'Kategoriya o\'chirildi')
        return redirect('category_list')

    return render(request, 'categories/delete.html', {'category': category})