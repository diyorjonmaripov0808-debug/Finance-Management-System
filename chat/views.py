from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from functools import wraps
from .models import Conversation, Message
from .forms import MessageForm
from users.models import User


def admin_required(view_func):
    """Faqat admin uchun"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, _('Ruxsat yo\'q'))
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_conversation_required(view_func):
    """Admin suhbati egasi bo'lishini tekshirish"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        conversation = get_object_or_404(Conversation, pk=conversation_id, is_deleted=False)
        
        if not request.user.is_staff:
            messages.error(request, _('Ruxsat yo\'q'))
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def chat_view(request):
    """User-dan admin-ga chat - foydalanuvchi sifatida ko'rish"""
    
    admin = User.objects.filter(is_staff=True, is_superuser=True).first()

    if not admin:
        messages.error(request, _('Admin topilmadi'))
        return redirect('dashboard')

    conversation, created = Conversation.objects.get_or_create(
        user=request.user,
        admin=admin,
        defaults={'is_deleted': False}
    )

    # Foydalanuvchi faolligini yangilash (view-ga kirganda)
    if not request.user.is_staff:
        User.objects.filter(id=request.user.id).update(updated_at=timezone.now())

    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    messages_list = conversation.messages.filter(is_deleted=False)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()

            return redirect('chat')
    else:
        form = MessageForm()

    context = {
        'conversation': conversation,
        'chat_messages': messages_list,
        'admin': admin,
        'form': form,
    }

    return render(request, 'chat/user_chat.html', context)


@login_required
@admin_required
def admin_chat_list_view(request):
    """Admin - barcha userlar bilan chatlar - faqat adminlar uchun dashboard"""

    conversations = Conversation.objects.filter(
        is_deleted=False
    ).select_related('user').prefetch_related('messages').order_by('-updated_at')

    # Har bir suhbat uchun qo'shimcha ma'lumotlar qo'shamiz
    for conv in conversations:
        conv.unread_count = conv.get_unread_count(request.user)
        last_msg = conv.messages.filter(is_deleted=False).last()
        conv.last_message = last_msg
        
        if last_msg:
            # So'nggi xabar kimdan kelganini aniqlash
            conv.last_message_from_me = (last_msg.sender == request.user)
            conv.waiting_reply = not conv.last_message_from_me
        else:
            conv.last_message_from_me = False
            conv.waiting_reply = False

    return render(request, 'chat/admin_chat_list.html', {'conversations': conversations})


@login_required
@admin_required
def admin_start_chat_view(request, user_id):
    """Bridge: Django Admin-dan chatga o'tish"""
    
    target_user = get_object_or_404(User, id=user_id)
    
    # Superuser uchun birinchi adminni olamiz yoki o'zini admin qilamiz
    admin_user = User.objects.filter(is_staff=True, is_superuser=True).first()
    
    conversation, created = Conversation.objects.get_or_create(
        user=target_user,
        admin=admin_user or request.user,
        defaults={'is_deleted': False}
    )
    
    return redirect('admin_chat_detail', conversation_id=conversation.id)


@login_required
@admin_conversation_required
def admin_chat_detail_view(request, conversation_id):
    """Admin - bitta user bilan chat - faqat admin"""

    conversation = get_object_or_404(
        Conversation,
        pk=conversation_id,
        is_deleted=False
    )

    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    messages_list = conversation.messages.filter(is_deleted=False)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()

            return redirect('admin_chat_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()

    context = {
        'conversation': conversation,
        'chat_messages': messages_list,
        'chat_user': conversation.user,
        'form': form,
    }

    return render(request, 'chat/admin_chat_detail.html', context)