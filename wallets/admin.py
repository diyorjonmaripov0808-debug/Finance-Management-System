from django.contrib import admin
from .models import Wallet


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_type', 'card_type', 'title', 'currency', 'balance', 'is_deleted', 'created_at')
    list_filter = ('wallet_type', 'currency', 'is_deleted', 'created_at')
    search_fields = ('user__phone_number', 'title', 'user__first_name', 'user__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('id', 'user', 'wallet_type', 'currency', 'balance')
        }),
        ('Karta ma\'lumotlari', {
            'fields': ('card_type', 'title'),
            'classes': ('collapse',)
        }),
        ('Holatlar', {
            'fields': ('is_deleted', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Wallet, WalletAdmin)
