from django.contrib import admin
from .models import Transfer


class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_wallet', 'to_wallet', 'from_amount', 'to_amount', 'exchange_rate', 'is_deleted', 'created_at')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('from_wallet__user__phone_number', 'to_wallet__user__phone_number')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Hamyonlar', {
            'fields': ('from_wallet', 'to_wallet')
        }),
        ('Miqdorlar', {
            'fields': ('from_amount', 'to_amount', 'exchange_rate')
        }),
        ('Holatlar', {
            'fields': ('is_deleted', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Transfer, TransferAdmin)
