from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin interface for CustomUser model.
    Extends Django's default UserAdmin with custom fields and configurations.
    """
    ordering = ['-date_joined', 'email']  # Most recent users first
    list_display = ['email', 'full_name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'is_superuser', 'date_joined']
    list_editable = ['is_active', 'is_staff']  # Allow quick editing of these fields
    list_per_page = 50  # Show more users per page
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('full_name', 'profile_image')}),  # Added profile_image
        (_('Permissions'), {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)  # Make permissions collapsible
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined', 'profile_updated_at'),
            'classes': ('collapse',)  # Make dates collapsible
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'full_name',
                'is_active', 'is_staff', 'profile_image'
            )
        }),
    )
    
    search_fields = ['email', 'full_name']  # Allow searching by name too
    readonly_fields = ('last_login', 'date_joined', 'profile_updated_at')
    
    def get_queryset(self, request):
        """Optimize queryset by selecting related fields"""
        return super().get_queryset(request).select_related('profile_image')

# Register the model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
