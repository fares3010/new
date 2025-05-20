from django.contrib import admin
from .models import Agent, AgentDocuments, AgentIntegrations, AgentEmbeddings

class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_id', 'name', 'user', 'visibility', 'created_at', 'is_deleted')
    search_fields = ('name', 'description', 'user__username')
    list_filter = ('visibility', 'is_deleted', 'is_archived', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('agent_id', 'created_at', 'updated_at')

class AgentDocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'document_name', 'document_type', 'created_at')
    search_fields = ('document_name', 'agent__name')
    list_filter = ('document_type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

class AgentIntegrationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'integration_type', 'status', 'created_at')
    search_fields = ('agent__name', 'integration_type')
    list_filter = ('integration_type', 'status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

class AgentEmbeddingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'embedding_type', 'created_at')
    search_fields = ('agent__name', 'embedding_type')
    list_filter = ('embedding_type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Agent, AgentAdmin)
admin.site.register(AgentDocuments, AgentDocumentsAdmin)
admin.site.register(AgentIntegrations, AgentIntegrationsAdmin)
admin.site.register(AgentEmbeddings, AgentEmbeddingsAdmin)
