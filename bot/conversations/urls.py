from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    path('', views.index, name='conversations-index'),
    path('list/', views.conversations, name='conversations-list'),
    path('<int:conversationId>/messages/', views.conversation_messages, name='conversation-messages'),
]
