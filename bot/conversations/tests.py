from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Conversation
from create_agent.models import Agent

class ConversationsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.agent = Agent.objects.create(user=self.user, name="Test Agent", description="desc")
        self.conversation1 = Conversation.objects.create(
            user=self.user,
            agent=self.agent,
            conversation_name="Test Conversation 1",
            is_archived=False,
            is_deleted=False,
            is_favorite=True,
            status="active"
        )
        self.conversation2 = Conversation.objects.create(
            user=self.user,
            agent=self.agent,
            conversation_name="Test Conversation 2",
            is_archived=True,
            is_deleted=False,
            is_favorite=False,
            status="completed"
        )

    def test_conversations_list_requires_authentication(self):
        url = reverse('conversations-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_conversations_list_returns_conversations(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('conversations-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertEqual(response.data['total'], 1)  # Only non-archived, non-deleted by default
        self.assertEqual(response.data['data'][0]['name'], "Test Conversation 1")

    def test_conversations_list_filter_archived(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('conversations-list')
        response = self.client.get(url, {'filter': 'archived'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 1)
        self.assertEqual(response.data['data'][0]['name'], "Test Conversation 2")

    def test_conversations_list_filter_favorite(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('conversations-list')
        response = self.client.get(url, {'filter': 'favorite'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 1)
        self.assertEqual(response.data['data'][0]['name'], "Test Conversation 1")

    def test_conversations_list_invalid_page_and_limit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('conversations-list')
        response = self.client.get(url, {'page': 'abc', 'limit': 'xyz'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_conversations_list_pagination(self):
        self.client.force_authenticate(user=self.user)
        # Add more conversations for pagination
        for i in range(15):
            Conversation.objects.create(
                user=self.user,
                agent=self.agent,
                conversation_name=f"Paginated {i}",
                is_archived=False,
                is_deleted=False,
                status="active"
            )
        url = reverse('conversations-list')
        response = self.client.get(url, {'page': 2, 'limit': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page'], 2)
        self.assertEqual(len(response.data['data']), 6)  # 16 total, 10 on page 1, 6 on page 2

    def test_conversations_list_page_exceeds_total(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('conversations-list')
        response = self.client.get(url, {'page': 100, 'limit': 10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
