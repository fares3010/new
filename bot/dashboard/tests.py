from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.cache import cache
from dashboard.models import Dashboard
from conversations.models import Conversation
from create_agent.models import Agent
import pytest

class DashboardTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data that will be used by all test methods
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        cls.dashboard = Dashboard.objects.create(
            user=cls.user,
            dashboard_type='test_dashboard',
            is_active=True
        )
        cls.client = Client()

    def setUp(self):
        # Clear cache before each test
        cache.clear()
        # Additional setup if needed
        self.dashboard.refresh_from_db()

    def tearDown(self):
        # Clean up after each test
        cache.clear()

    def test_dashboard_creation(self):
        """Test basic dashboard creation and attributes"""
        self.assertIsNotNone(self.dashboard.dashboard_id)
        self.assertEqual(self.dashboard.user, self.user)
        self.assertEqual(self.dashboard.dashboard_type, 'test_dashboard')
        self.assertTrue(self.dashboard.is_active)
        self.assertFalse(self.dashboard.is_deleted)
        self.assertIsNotNone(self.dashboard.created_at)
        self.assertIsNotNone(self.dashboard.updated_at)

    @pytest.mark.django_db
    def test_dashboard_stats_with_data(self):
        """Test dashboard stats with actual conversation data"""
        # Create test conversations
        conversation = Conversation.objects.create(
            user=self.user,
            is_active=True,
            number_of_agent_messages=5
        )
        
        # Test stats after data creation
        self.dashboard.update_stats()
        
        # Test conversation stats
        self.assertEqual(self.dashboard.total_conversations(), 1)
        self.assertEqual(self.dashboard.active_conversations(), 1)
        self.assertEqual(self.dashboard.inactive_conversations(), 0)
        
        # Test response stats
        self.assertEqual(self.dashboard.total_responses(), 5)
        
        # Test change rates
        self.assertIsInstance(self.dashboard.conversations_change_rate(), float)
        self.assertIsInstance(self.dashboard.active_conversations_change_rate(), float)

    def test_dashboard_stats_empty(self):
        """Test dashboard stats with no data"""
        self.dashboard.update_stats()
        
        # Test all stats return expected default values
        stats = {
            'total_conversations': 0,
            'active_conversations': 0,
            'inactive_conversations': 0,
            'total_of_agents': 0,
            'active_agents': 0,
            'inactive_agents': 0,
            'avg_response_time': 0,
            'user_satisfaction_rate': 0
        }
        
        for stat_name, expected_value in stats.items():
            method = getattr(self.dashboard, stat_name)
            self.assertEqual(method(), expected_value, f"{stat_name} failed")

    def test_dashboard_admin_access(self):
        """Test admin interface access and permissions"""
        # Test unauthorized access
        response = self.client.get(reverse('admin:dashboard_dashboard_changelist'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
        
        # Test authorized access
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('admin:dashboard_dashboard_changelist'))
        self.assertEqual(response.status_code, 200)
        
        # Test specific dashboard access
        response = self.client.get(
            reverse('admin:dashboard_dashboard_change', args=[self.dashboard.dashboard_id])
        )
        self.assertEqual(response.status_code, 200)

    def test_dashboard_cache(self):
        """Test caching of dashboard statistics"""
        # First call should hit the database
        first_call = self.dashboard.total_conversations()
        
        # Second call should use cache
        second_call = self.dashboard.total_conversations()
        
        self.assertEqual(first_call, second_call)
        
        # Clear cache and verify new database hit
        cache.clear()
        third_call = self.dashboard.total_conversations()
        self.assertEqual(first_call, third_call)

    def test_dashboard_last_week_data(self):
        """Test last week's conversation and response data"""
        last_week_conversations = self.dashboard.last_week_conversations()
        last_week_responses = self.dashboard.last_week_responses()
        
        self.assertIsInstance(last_week_conversations, dict)
        self.assertIsInstance(last_week_responses, list)
        self.assertEqual(len(last_week_responses), 7)
        self.assertEqual(len(last_week_conversations), 7)

    def test_dashboard_error_handling(self):
        """Test error handling in dashboard methods"""
        # Test with invalid data
        self.dashboard.dashboard_type = None
        with self.assertRaises(Exception):
            self.dashboard.save()
        
        # Test with invalid user
        self.dashboard.user = None
        with self.assertRaises(Exception):
            self.dashboard.save()