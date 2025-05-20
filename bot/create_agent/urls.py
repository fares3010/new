from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('agents/', views.agent_list, name='agent-list'),
    path('agents/<int:pk>/', views.agent_detail, name='agent-detail'),
    path('agents/create/', views.create_agent, name='agent-create'),
    path('agents/<int:pk>/update/', views.update_agent, name='agent-update'),
    path('agents/<int:pk>/delete/', views.delete_agent, name='agent-delete'),
]