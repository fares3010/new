from django.shortcuts import render # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view

@api_view(['GET'])
def dashboard_stats(request):
 x = {
     "totalConversations": 0,
     "activeUsers": 0,
     "avgResponseTime": "0s",
     "userSatisfaction": "0%",
     "trends": { "conversations": {"value": 12 , "isPositive" : True},
                   "users": {"value": 2 , "isPositive" : False},
                   "responseTime": {"value": 1 , "isPositive" : True},
                   "satisfaction": {"value": 3 , "isPositive" : True} 
                
               }
    }

 return Response(x)

@api_view(['GET'])
def recent_chats(request):
    no_of_chats = request.GET.get('count', None)   

    x = [{
        "id": 1,
         "name": "John Doe",
         "lastMessage": "Hello, how can I help you?",
         "timestamp": "2023-10-01T12:00:00Z",
         "unread": False,
         "status": "active",
    },
    {
        "id": 2,
         "name": "Jane Smith",
         "lastMessage": "I need assistance with my order.",
         "timestamp": "2023-10-01T12:05:00Z",
         "unread": True,
         "status": "completed",
    },
    {
        "id": 3,
         "name": "Alice Johnson",
         "lastMessage": "Can you provide more details?",
         "timestamp": "2023-10-01T12:10:00Z",
         "unread": False,
         "status": "active",
    },
    {
        "id": 4,
         "name": "Bob Brown",
         "lastMessage": "I have a question about my account.",
         "timestamp": "2023-10-01T12:15:00Z",
         "unread": True,
         "status": "completed",
    },
    {
        "id": 5,
         "name": "Charlie Green",
         "lastMessage": "What are the latest updates?",
         "timestamp": "2023-10-01T12:20:00Z",
         "unread": False,
         "status": "active",
    }]

    return Response(x)

@api_view(['GET'])
def engagement_stats(request):
    stats_range = request.GET.get('range', None)
    x = [{
        "name": "Sat",
        "conversations": 10,
        "responses": 15,  
    },
    {
        "name": "Sun",
        "conversations": 12,
        "responses": 18,  
    },
    {
        "name": "Mon",
        "conversations": 8,
        "responses": 10,  
    },
    {
        "name": "Tue",
        "conversations": 15,
        "responses": 20,  
    },
    {
        "name": "Wed",
        "conversations": 20,
        "responses": 25,  
    },
    {
        "name": "Thu",
        "conversations": 18,
        "responses": 22,  
    },
    {
        "name": "Fri",
        "conversations": 25,
        "responses": 30,  
    }]

    return Response(x)

@api_view(['GET'])
def api_health_check(request):
    return Response({"status": "ok",
                     "version": "1.0.0",
                     "timestamp": "2023-10-01T12:00:00Z",
                    })








