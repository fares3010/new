from django.urls import path
from . import views

app_name = 'integrations'

urlpatterns = [
    path('', views.get_integrations, name='get_integrations'),
    path('categories/', views.get_integration_categories, name='get_integration_categories'),
]
                