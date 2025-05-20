"""
URL configuration for bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface
    path("admin/", admin.site.urls),
    
    # Authentication
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("auth/", include("allauth.urls")),
    
    # App routes - using namespaced URLs for better organization
    path("conversations/", include("conversations.urls", namespace="conversations")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("plans/", include("usage_plans.urls", namespace="plans")),
    path("agents/", include("create_agent.urls", namespace="agents")),
    path("integrations/", include("integrations.urls", namespace="integrations")),
]
