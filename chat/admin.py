from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'created_at')
    fields = ('sender', 'text', 'is_read', 'created_at')


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin', 'get_message_count', 'is_deleted', 'updated_at')
    list_filter = ('is_deleted', 'updated_at', 'created_at')
    search_fields = ('user__phone_number', 'admin__username', 'user__first_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
    inlines = [MessageInline]
    
    def get_message_count(self, obj):
        return obj.messages.filter(is_deleted=False).count()
    get_message_count.short_description = 'Xabarlar soni'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'text_preview', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'conversation__admin')
    search_fields = ('sender__phone_number', 'text', 'conversation__user__first_name')
    readonly_fields = ('id', 'conversation', 'sender', 'created_at')
    ordering = ('-created_at',)
    
    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Xabar'
    
    def has_add_permission(self, request):
        return False


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
