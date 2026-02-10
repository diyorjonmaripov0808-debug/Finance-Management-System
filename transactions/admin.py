from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'category', 'amount', 'currency', 'exchange_rate', 'is_deleted', 'created_at')
    list_filter = ('category__type', 'currency', 'is_deleted', 'created_at')
    search_fields = ('wallet__user__phone_number', 'category__name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Hamyon va Kategoriya', {
            'fields': ('wallet', 'category')
        }),
        ('Ma\'lumotlar', {
            'fields': ('amount', 'currency', 'exchange_rate', 'description')
        }),
        ('Holatlar', {
            'fields': ('is_deleted', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Transaction, TransactionAdmin)
