from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Agent
from .serializers import AgentSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def agent_list(request):
    """
    List all agents for the current user.
    Returns a list of active (non-deleted) agents.
    """
    try:
        agents = Agent.objects.filter(user=request.user, is_deleted=False)
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {"error": "An unexpected error occurred while retrieving agents"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def agent_detail(request, pk):
    """
    Get a single agent's details.
    Returns 404 if agent not found or doesn't belong to user.
    """
    try:
        agent = get_object_or_404(Agent, pk=pk, user=request.user, is_deleted=False)
        serializer = AgentSerializer(agent)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Agent.DoesNotExist:
        return Response(
            {"error": "Agent not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_agent(request):
    """
    Create a new agent.
    Returns 201 on success, 400 on validation error.
    """
    try:
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(
            {"error": "An unexpected error occurred while creating an agent"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_agent(request, pk):
    """
    Update an existing agent.
    Returns 200 on success, 404 if not found, 400 on validation error.
    """
    try:
        agent = get_object_or_404(Agent, pk=pk, user=request.user, is_deleted=False)
        serializer = AgentSerializer(agent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Agent.DoesNotExist:
        return Response(
            {"error": "Agent not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )   

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_agent(request, pk):
    """
    Soft delete an existing agent.
    Returns 204 on success, 404 if not found.
    """
    try:
        agent = get_object_or_404(Agent, pk=pk, user=request.user, is_deleted=False)
        agent.is_deleted = True
        agent.save(update_fields=['is_deleted'])
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Agent.DoesNotExist:
        return Response(
            {"error": "Agent not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
