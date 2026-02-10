from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PhoneOTP


from django.utils.html import format_html
from django.urls import reverse

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('phone_number', 'auth_status', 'is_deleted')}),
    )
    list_display = (
        'phone_number', 'first_name', 'last_name', 
        'auth_status', 'is_staff', 'is_active', 
        'chat_link', 'created_at'
    )
    list_filter = ('auth_status', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'chat_link', 'created_at', 'updated_at')

    def chat_link(self, obj):
        if obj.is_staff:
            return "-"
        url = reverse('admin_start_chat', args=[obj.id])
        return format_html('<a class="button" href="{}">Chat</a>', url)
    chat_link.short_description = "Chat"


class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_code', 'confirmed', 'code_expires_at', 'is_expired', 'created_at')
    list_filter = ('confirmed', 'created_at', 'code_expires_at')
    search_fields = ('user__phone_number', 'verification_code')
    readonly_fields = ('id', 'created_at', 'updated_at', 'is_expired')
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.short_description = "Muddat tugganmi?"
    is_expired.boolean = True


admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)
