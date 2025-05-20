from django.contrib import admin
from .models import SubscriptionPlan, PlanFeature, UserSubscription
from django.contrib.auth.models import User
from django.utils import timezone


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 1
    readonly_fields = ('created_at', 'updated_at')
    fields = ('feature_name', 'feature_type', 'feature_description', 'feature_limit', 'is_active', 'created_at', 'updated_at')

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'plan_price', 'plan_period', 'is_active', 'created_at')
    list_filter = ('is_active', 'plan_period')
    search_fields = ('plan_name', 'plan_description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PlanFeatureInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('plan_name', 'plan_description', 'plan_price', 'plan_period')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name', 'plan', 'feature_type', 'feature_limit', 'is_active', 'created_at')
    list_filter = ('is_active', 'feature_type')
    search_fields = ('feature_name', 'feature_description', 'plan__plan_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Feature Information', {
            'fields': ('plan', 'feature_name', 'feature_type', 'feature_description', 'feature_limit')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscription_id', 'user', 'plan', 'is_active', 'usage_start_date', 'created_at')
    list_filter = ('is_active', 'is_deleted', 'plan')
    search_fields = ('user__username', 'user__email', 'stripe_subscription_id')
    readonly_fields = ('subscription_id', 'created_at', 'updated_at', 'usage_start_date')
    
    fieldsets = (
        ('Subscription Information', {
            'fields': ('user', 'plan', 'stripe_subscription_id', 'usage_start_date')
        }),
        ('Status', {
            'fields': ('is_active', 'is_deleted')
        }),
        ('Additional Information', {
            'fields': ('meta_data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

# Register models with their admin classes
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(PlanFeature, PlanFeatureAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)