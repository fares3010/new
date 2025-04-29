from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path("api/dashboard/stats", views.dashboard_stats, name="dashboard_stats"),
    path("api/dashboard/recent-chats", views.recent_chats, name="recent_chats"),
    path("api/dashboard/engagement", views.engagement_stats, name="engagement_stats"),
    path("api/health", views.api_health_check, name="api_health_check"),
]
