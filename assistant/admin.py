from django.contrib import admin
from .models import UserSession, Conversation

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user_type', 'created_at', 'updated_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['session_id']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_preview', 'is_user', 'timestamp']
    list_filter = ['is_user', 'timestamp']
    search_fields = ['message']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'