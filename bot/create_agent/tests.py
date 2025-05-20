from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Agent, AgentDocuments, AgentIntegrations, AgentWebsites
from django.utils import timezone
from datetime import timedelta
import json

class AgentModelTests(TestCase):
    def setUp(self):
        """Set up test data for agent model tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.agent = Agent.objects.create(
            user=self.user,
            name='Test Agent',
            description='A test agent',
            visibility='private'
        )

    def test_agent_creation(self):
        """Test that an agent can be created with basic fields"""
        self.assertEqual(self.agent.name, 'Test Agent')
        self.assertEqual(self.agent.description, 'A test agent')
        self.assertEqual(self.agent.visibility, 'private')
        self.assertFalse(self.agent.is_deleted)
        self.assertFalse(self.agent.is_archived)
        self.assertFalse(self.agent.is_favorite)
        self.assertIsNotNone(self.agent.created_at)
        self.assertIsNotNone(self.agent.updated_at)

    def test_agent_str_method(self):
        """Test the string representation of an agent"""
        expected_str = f"Test Agent (ID: {self.agent.agent_id})"
        self.assertEqual(str(self.agent), expected_str)

    def test_agent_is_active(self):
        """Test the is_active method of an agent"""
        self.assertFalse(self.agent.is_active())
        
        # Test with recent conversation
        self.agent.last_conversation_at = timezone.now()
        self.agent.save()
        self.assertTrue(self.agent.is_active())

class AgentDocumentsTests(TestCase):
    def setUp(self):
        """Set up test data for document tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.agent = Agent.objects.create(
            user=self.user,
            name='Test Agent'
        )
        self.document = AgentDocuments.objects.create(
            agent=self.agent,
            document_name='Test Document',
            document_url='https://example.com/test.pdf',
            document_format='PDF',
            document_size=1024
        )

    def test_document_creation(self):
        """Test that a document can be created with basic fields"""
        self.assertEqual(self.document.document_name, 'Test Document')
        self.assertEqual(self.document.document_format, 'PDF')
        self.assertEqual(self.document.document_size, 1024)
        self.assertTrue(self.document.is_active)
        self.assertFalse(self.document.is_deleted)
        self.assertIsNotNone(self.document.created_at)
        self.assertIsNotNone(self.document.updated_at)

    def test_document_formatted_size(self):
        """Test the formatted_size property for different sizes"""
        # Test KB
        self.assertEqual(self.document.formatted_size, '1.00 KB')
        
        # Test MB
        self.document.document_size = 1024 * 1024
        self.document.save()
        self.assertEqual(self.document.formatted_size, '1.00 MB')
        
        # Test GB
        self.document.document_size = 1024 * 1024 * 1024
        self.document.save()
        self.assertEqual(self.document.formatted_size, '1.00 GB')

    def test_document_get_file_type_icon(self):
        """Test the get_file_type_icon method for different formats"""
        self.assertEqual(self.document.get_file_type_icon(), '📄')
        
        # Test other formats
        self.document.document_format = 'DOC'
        self.document.save()
        self.assertEqual(self.document.get_file_type_icon(), '📝')
        
        self.document.document_format = 'XLS'
        self.document.save()
        self.assertEqual(self.document.get_file_type_icon(), '📊')

class AgentIntegrationsTests(TestCase):
    def setUp(self):
        """Set up test data for integration tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.agent = Agent.objects.create(
            user=self.user,
            name='Test Agent'
        )
        self.integration = AgentIntegrations.objects.create(
            agent=self.agent,
            integration_name='Test Integration',
            integration_category='CRM',
            integration_priority=1,
            integration_url='https://example.com/api'
        )

    def test_integration_creation(self):
        """Test that an integration can be created with basic fields"""
        self.assertEqual(self.integration.integration_name, 'Test Integration')
        self.assertEqual(self.integration.integration_category, 'CRM')
        self.assertEqual(self.integration.integration_priority, 1)
        self.assertEqual(self.integration.integration_url, 'https://example.com/api')
        self.assertIsNotNone(self.integration.created_at)
        self.assertIsNotNone(self.integration.updated_at)

class AgentWebsitesTests(TestCase):
    def setUp(self):
        """Set up test data for website tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.agent = Agent.objects.create(
            user=self.user,
            name='Test Agent'
        )
        self.website = AgentWebsites.objects.create(
            agent=self.agent,
            website_url='https://example.com',
            website_name='Test Website',
            website_type='blog',
            crawl_frequency='daily'
        )

    def test_website_creation(self):
        """Test that a website can be created with basic fields"""
        self.assertEqual(self.website.website_url, 'https://example.com')
        self.assertEqual(self.website.website_name, 'Test Website')
        self.assertEqual(self.website.website_type, 'blog')
        self.assertEqual(self.website.crawl_frequency, 'daily')
        self.assertIsNotNone(self.website.created_at)
        self.assertIsNotNone(self.website.updated_at)

    def test_website_should_crawl(self):
        """Test the should_crawl method for different scenarios"""
        # Should crawl initially as last_crawled_at is None
        self.assertTrue(self.website.should_crawl())
        
        # Set last_crawled_at to now
        self.website.last_crawled_at = timezone.now()
        self.website.save()
        self.assertFalse(self.website.should_crawl())
        
        # Test with different crawl frequencies
        self.website.crawl_frequency = 'hourly'
        self.website.last_crawled_at = timezone.now() - timedelta(hours=2)
        self.website.save()
        self.assertTrue(self.website.should_crawl())

    def test_website_get_domain(self):
        """Test the get_domain method for different URLs"""
        self.assertEqual(self.website.get_domain(), 'example.com')
        
        # Test with subdomain
        self.website.website_url = 'https://blog.example.com'
        self.website.save()
        self.assertEqual(self.website.get_domain(), 'blog.example.com')
        
        # Test with path
        self.website.website_url = 'https://example.com/path'
        self.website.save()
        self.assertEqual(self.website.get_domain(), 'example.com')

class AgentAPITests(TestCase):
    def setUp(self):
        """Set up test data for API tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.agent = Agent.objects.create(
            user=self.user,
            name='Test Agent',
            description='A test agent',
            visibility='private'
        )

    def test_create_agent(self):
        """Test creating a new agent via API"""
        url = reverse('create_agent')
        data = {
            'name': 'New Test Agent',
            'description': 'A new test agent',
            'visibility': 'private'
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Agent.objects.filter(name='New Test Agent').exists())
        
        # Verify response data
        response_data = json.loads(response.content)
        self.assertEqual(response_data['name'], 'New Test Agent')
        self.assertEqual(response_data['visibility'], 'private')

    def test_get_agent_list(self):
        """Test retrieving the list of agents"""
        url = reverse('agent_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verify response data
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['name'], 'Test Agent')

    def test_get_agent_detail(self):
        """Test retrieving a specific agent's details"""
        url = reverse('agent_detail', args=[self.agent.agent_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verify response data
        response_data = json.loads(response.content)
        self.assertEqual(response_data['name'], 'Test Agent')
        self.assertContains(response, 'Test Agent')
        self.assertContains(response, 'A test agent')


    def test_update_agent(self):
        """Test updating an existing agent via API"""
        url = reverse('agent_detail', args=[self.agent.agent_id])
        data = {
            'name': 'Updated Test Agent',
            'description': 'An updated test agent',
            'visibility': 'public'
        }
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.agent.refresh_from_db()
        self.assertEqual(self.agent.name, 'Updated Test Agent')
        self.assertEqual(self.agent.visibility, 'public')

    def test_delete_agent(self):
        """Test deleting an agent via API"""
        url = reverse('agent_detail', args=[self.agent.agent_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Agent.objects.filter(agent_id=self.agent.agent_id, is_deleted=True).exists())

    def test_get_nonexistent_agent(self):
        """Test retrieving a non-existent agent"""
        url = reverse('agent_detail', args=[99999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_agent_validation(self):
        """Test agent creation validation"""
        url = reverse('create_agent')
        # Test missing required field
        data = {'description': 'Missing name field'}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test invalid visibility value
        data = {
            'name': 'Invalid Agent',
            'description': 'Test agent',
            'visibility': 'invalid_value'
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_unauthorized_access(self):
        """Test unauthorized access to agent endpoints"""
        self.client.logout()
        
        # Test getting agent list
        url = reverse('agent_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        # Test getting agent detail
        url = reverse('agent_detail', args=[self.agent.agent_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

