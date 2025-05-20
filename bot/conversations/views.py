from datetime import date
from django.shortcuts import render
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view
from rest_framework import status # type: ignore
from .models import Conversation  
from django.http import JsonResponse
import math

@api_view(["GET"])
def conversations(request):
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
    filter_param = request.GET.get("filter", None) 
    try:
       page = int(request.GET.get("page", 1))
       limit = int(request.GET.get("limit", 10))
    except ValueError:
        return Response({"error": "Page and limit must be integers."}, status=status.HTTP_400_BAD_REQUEST)
    
    qs = Conversation.objects.filter(user=request.user)
    if not qs.exists():
        return Response({"error": "No recent conversations found."}, status=status.HTTP_404_NOT_FOUND)
        

    # Enhanced filtering logic for maintainability, extensibility, and clarity

    # Define a mapping of filter parameters to their corresponding queryset filters
    filter_map = {
        "active": {"status": "active"},
        "completed": {"status": "completed"},
        "archived": {"is_archived": True},
        "unread": {"status": "unread"},
        "deleted": {"is_deleted": True},
        "favorite": {"is_favorite": True},
    }

    # If a valid filter_param is provided, apply its filter; otherwise, show only non-archived, non-deleted conversations
    if filter_param and filter_param in filter_map:
        qs = qs.filter(**filter_map[filter_param])
    else:
        qs = qs.filter(is_archived=False, is_deleted=False)


    # Use the filtered queryset (qs) to count conversations after all filters are applied
    total = qs.count()
    # Calculate the total number of pages, rounding up for any partial page
    no_of_pages = math.ceil(total / limit) if limit > 0 else 0

    # Validate pagination parameters
    if page < 1:
        return Response({"error": "Page number must be at least 1."}, status=status.HTTP_400_BAD_REQUEST)
    if limit < 1 or limit > 100:
        return Response({"error": "Limit must be between 1 and 100."}, status=status.HTTP_400_BAD_REQUEST)
    if no_of_pages > 0 and page > no_of_pages:
        return Response({"error": "Page number exceeds total pages."}, status=status.HTTP_400_BAD_REQUEST)

    offset = (page - 1) * limit
    end = offset + limit

    


    if total == 0:
        return Response({"error": "No conversations found."},
                        status=status.HTTP_404_NOT_FOUND)
    
    conversations = qs.order_by('-last_message_time')[offset:end]  
   
    

    data = []
    for conversation in conversations:
        # Defensive checks for agent and method existence
        agent = getattr(conversation, "agent", None)
        agent_id = getattr(agent, "agent_id", None) if agent else None
        agent_name = getattr(agent, "name", None) if agent else None

        # Use getattr with defaults for methods/fields that may not exist
        last_message_text = conversation.last_message_text() if hasattr(conversation, "last_message_text") else None
        last_message_time = conversation.last_message_time() if hasattr(conversation, "last_message_time") else None
        unread = conversation.check_last_message_is_read() if hasattr(conversation, "check_last_message_is_read") else None
        status = conversation.check_is_active() if hasattr(conversation, "check_is_active") else getattr(conversation, "status", None)

        data.append({
            "id": getattr(conversation, "conversation_id", None),
            "name": getattr(conversation, "conversation_name", None),
            "lastMessage": last_message_text,
            "timestamp": last_message_time,
            "unread": unread,
            "status": status,
            "agent_id": agent_id,
            "agent_name": agent_name,
        })
    

    # Prepare the response data
    # Improved response formatting and added isLoading, error, and refetch fields for consistency with other endpoints.
    response_data = {
        "data": data,                # List of conversations
        "total": int(total),         # Total number of conversations matching the filter
        "page": int(page),           # Current page number
        "limit": int(limit),         # Items per page
        "totalPages": int(no_of_pages), # Total number of pages available
        "isLoading": False,          # Loading state
        "error": None,               # Error state
        "refetch": False,            # Refetch state
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
def conversation_messages(request, conversationId):
    """
    Retrieve all messages for a given conversation, ensuring the user is authenticated
    and authorized to access the conversation.
    """
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Validate conversationId
    if not conversationId:
        return Response(
            {"error": "Conversation ID is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Fetch the conversation, ensuring it belongs to the user
    try:
        conversation = Conversation.objects.get(conversation_id=conversationId, user=request.user)
    except Conversation.DoesNotExist:
        return Response(
            {"error": "Conversation not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Retrieve messages, most recent first
    messages_qs = conversation.messages.order_by('-message_time')
    if not messages_qs.exists():
        return Response(
            {"error": "No messages found."},
            status=status.HTTP_404_NOT_FOUND
        )
    # Use the correct queryset variable and improve field naming/consistency.
    data = []
    for message in messages_qs:
        data.append({
            "id": message.message_id,
            "content": message.message_text,
            "sender": message.sender_type,
            "timestamp": message.message_time,
            "conversationId": message.conversation.conversation_id,  # Fixed typo from "conversaionId"
            "isRead": message.is_read,
            "isDeleted": message.is_deleted,
            "isArchived": message.is_archived,
            "attachments": [
                {
                    "attachment_id": att.attachment_id,
                    "attachment_name": att.attachment_name,
                    "attachment_path": att.attachment_path,
                    "attachment_type": att.attachment_type,
                    "attachment_size": att.attachment_size,
                }
                for att in message.attachments.all()
            ] if hasattr(message, "attachments") else [],
        })

    response_data = { 
        "data": data,  # List of messages
        "isLoading": False,  # Loading state
        "error": None,  # Error state
        "refetch": False,  # Refetch state
    }

    return Response(response_data, status=status.HTTP_200_OK)

# The index view provides a simple JSON response indicating the Conversations API is available.
# It can be used as a health check or landing endpoint for the API.
def index(request):
    return JsonResponse({'message': 'Conversations API'})
