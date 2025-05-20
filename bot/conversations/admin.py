from django.contrib import admin
from .models import (
    Conversation,
    ConversationMessages,
    ConversationAttachments,
    ConversationTag,
    ConversationNotes,
    ConversationFeedback,
)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation_name', 'user', 'agent', 'status', 'is_archived', 'is_deleted', 'is_favorite')
    list_filter = ('status', 'is_archived', 'is_deleted', 'is_favorite')
    search_fields = ('conversation_name', 'user__username', 'agent__name')
    ordering = ('-id',)
    readonly_fields = ('id',)

@admin.register(ConversationMessages)
class ConversationMessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender_id', 'sender_type', 'message_text', 'message_time', 'is_read', 'is_deleted', 'is_archived')
    list_filter = ('is_read', 'is_deleted', 'is_archived')
    search_fields = ('conversation__conversation_name', 'sender__username')
    ordering = ('-id',)
    readonly_fields = ('id',)

@admin.register(ConversationAttachments)
class ConversationAttachmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'attachment_name', 'attachment_path', 'attachment_type', 'attachment_size')
    list_filter = ('attachment_type',)
    search_fields = ('message__conversation__conversation_name', 'attachment_name')
    ordering = ('-id',)

@admin.register(ConversationTag)
class ConversationTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'tag_name', 'created_at', 'updated_at', 'is_active', 'is_deleted')
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('conversation__conversation_name', 'tag_name')
    ordering = ('-id',)

@admin.register(ConversationNotes)
class ConversationNotesAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'note_text', 'created_at', 'updated_at', 'is_active', 'is_deleted')
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('conversation__conversation_name', 'note_text')
    ordering = ('-id',) 

@admin.register(ConversationFeedback)
class ConversationFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'feedback_text', 'rating', 'created_at', 'updated_at', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('conversation__conversation_name', 'feedback_text')
    ordering = ('-id',) 




