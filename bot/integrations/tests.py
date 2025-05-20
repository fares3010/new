from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient   
from .models import Integration, IntegrationCategory            

class IntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.integration_data = {
            "agent_id": 1,
            "integration_name": "Test Integration",
            "integration_type": "api",
            "integration_url": "https://test.com/api",
            "integration_key": "test_key",
            "integration_secret": "test_secret",
            "integration_token": "test_token",
            "description": "Test description",
            "is_active": True,
        }
        self.category_data = {
            "category_name": "Test Category",
            "description": "Test description",
            "is_active": True,
        }

    def test_create_integration(self):
        url = reverse('get_integrations')
        response = self.client.post(url, self.integration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Integration.objects.count(), 1)
        self.assertEqual(Integration.objects.get().integration_name, 'Test Integration')

    def test_get_integrations(self):
        url = reverse('get_integrations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['integration_name'], 'Test Integration')

    def test_get_integration_categories(self):
        url = reverse('get_integration_categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['category_name'], 'Test Category')

    def test_update_integration(self):
        url = reverse('get_integrations')
        response = self.client.put(url, self.integration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Integration.objects.get().integration_name, 'Updated Integration')

    def test_delete_integration(self):
        url = reverse('get_integrations')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Integration.objects.count(), 0)    

    def test_create_integration_category(self):
        url = reverse('get_integration_categories')
        response = self.client.post(url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IntegrationCategory.objects.count(), 1)
        self.assertEqual(IntegrationCategory.objects.get().category_name, 'Test Category')

    def test_get_integration_categories(self):
        url = reverse('get_integration_categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['category_name'], 'Test Category')

    def test_update_integration_category(self):
        url = reverse('get_integration_categories')
        response = self.client.put(url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(IntegrationCategory.objects.get().category_name, 'Updated Category')

    def test_delete_integration_category(self):
        url = reverse('get_integration_categories')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(IntegrationCategory.objects.count(), 0)            
