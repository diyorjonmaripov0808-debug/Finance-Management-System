from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user', 'is_deleted', 'created_at')
    list_filter = ('type', 'is_deleted', 'created_at')
    search_fields = ('name', 'user__phone_number', 'user__first_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


admin.site.register(Category, CategoryAdmin)
