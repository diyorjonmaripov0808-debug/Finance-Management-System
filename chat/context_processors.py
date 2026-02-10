from .models import Conversation, Message

def unread_messages_count(request):
    """
    Istalgan sahifada o'qilmagan xabarlar sonini olish uchun context processor.
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Admin uchun barcha o'zi biriktirilgan (yoki barcha) o'qilmagan xabarlar soni
            # Bizning holatda admin barcha o'qilmagan xabarlarni ko'rishi maqsadga muvofiq
            count = Message.objects.filter(
                is_read=False
            ).exclude(sender=request.user).count()
        else:
            # Oddiy user uchun o'zining suhbatidagi o'qilmagan xabarlar soni
            count = Message.objects.filter(
                conversation__user=request.user,
                is_read=False
            ).exclude(sender=request.user).count()
        
        return {'global_unread_count': count}
    
    return {'global_unread_count': 0}
