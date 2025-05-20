from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Integration, IntegrationCategory

# Create your views here.

@api_view(["GET"])
def get_integrations(request):
    """
    Retrieve all integrations with optional filtering by agent ID.

    Args:
        request: HTTP request object    

    Returns:
        Response: JSON response containing all integrations or filtered by agent ID
    """
    agent_id = request.query_params.get("agent_id")
    if agent_id:
        integrations = Integration.objects.filter(agent_id=agent_id)
    else:
        integrations = Integration.objects.all()

    integration_list = []
    for integration in integrations:
        integration_list.append(integration.to_dict())

    return Response(integration_list, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_integration_categories(request):
    """
    Retrieve all integration categories.

    Returns:
        Response: JSON response containing all integration categories
    """
    categories = IntegrationCategory.objects.all()  
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())

    return Response(category_list, status=status.HTTP_200_OK)                               



