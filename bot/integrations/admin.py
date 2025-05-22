from django.contrib import admin
from .models import Integration, IntegrationCategory

# Register your models here.

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('integration_id', 'agent',"integration_name", 'integration_type', 'created_at', 'is_active')
    search_fields = ('integration_name', 'integration_type', 'description')
    list_filter = ('integration_type', 'created_at', 'is_active')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    list_editable = ('is_active',)

@admin.register(IntegrationCategory)
class IntegrationCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'agent', 'category_name', 'created_at', 'is_active')
    search_fields = ('category_name', 'description')
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    list_editable = ('is_active',)