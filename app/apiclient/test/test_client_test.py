"""
Tests for client APIs.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse 
from rest_framework import status
from rest_framework.test import APIClient
from core.models import (Cliente)
from apiclient.serializers import (
    apiClientSerializer,
    apiClientDetailSerializer,
)
 
 
CLIENTES_URL = reverse('apiclient:cliente-list')
 
 
def detail_url(client_id):
    """Create and return a client detail URL."""
    return reverse('apiclient:cliente-detail', args=[client_id])
 
 
def create_client(user, **params):
    """Create and return a sample client."""
    defaults = {
        'nombre' : 'Sample Client name',
        'email' : 'Sample@gmail.com',
        'telefono' : '123456789'        
    }
    defaults.update(params)
 
    client = Cliente.objects.create(user=user, **defaults)
    return client
 
 
def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)
 
 # TEST CLASS
class PublicClientAPITests(TestCase):
    """Test unauthenticated API requests."""
 
    def setUp(self):
        self.client = APIClient()
 
    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CLIENTES_URL)
 
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
 
 
class PrivateClientpiTests(TestCase):
    """Test authenticated API requests."""
 
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='cliente@example.com', password='test123')
        self.client.force_authenticate(self.user)
 
    def test_retrieve_clients(self):
        """Test retrieving a list of clients."""
        create_client(user=self.user)
        create_client(user=self.user)
 
        res = self.client.get(CLIENTES_URL)
 
        clients = Cliente.objects.all().order_by('-id')
        serializer = apiClientSerializer(clients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
 
    def test_client_list_limited_to_user(self):
        """Test list of clients is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_client(user=other_user)
        create_client(user=self.user)
 
        res = self.client.get(CLIENTES_URL)
 
        clients = Cliente.objects.filter(user=self.user)
        serializer = apiClientSerializer(clients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
 
    def test_get_client_detail(self):
        """Test get client detail."""
        client = create_client(user=self.user)
 
        url = detail_url(client.id)
        res = self.client.get(url)
 
        serializer = apiClientDetailSerializer(client)
        self.assertEqual(res.data, serializer.data)
 
    def test_create_client(self):
        """Test creating a client."""
        payload = {
            'nombre': 'Sample client',
            'email': 'sample@gmail.com',
            'telefono': '123546546546464456789'
        }
        res = self.client.post(CLIENTES_URL, payload)
 
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        client = Cliente.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(client, k), v)
        self.assertEqual(client.user, self.user)
 
    def test_partial_update(self):
        """Test partial update of a client."""        
        client = create_client(
            user=self.user,
            nombre='Sample client title partial no phone',
            email ='sample@gmail.com',            
        )
 
        payload = {'nombre': 'New client title'}
        url = detail_url(client.id)
        res = self.client.patch(url, payload)
 
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        client.refresh_from_db()
        self.assertEqual(client.nombre, payload['nombre'])        
        self.assertEqual(client.user, self.user)
 
    def test_full_update(self):
        """Test full update of client."""
        client = create_client(
            user=self.user,
            nombre='Sample client title',
            email='Sample@gamil.com',           
            telefono='123456789',
        )
 
        payload = {
            'nombre':'Sample client title',
            'email':'Sample@gamil.com',           
            'telefono':'123456789',
        }
        url = detail_url(client.id)
        res = self.client.put(url, payload)
 
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        client.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(client, k), v)
        self.assertEqual(client.user, self.user)
 
    def test_update_user_returns_error(self):
        """Test changing the client user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        client = create_client(user=self.user)
 
        payload = {'user': new_user.id}
        url = detail_url(client.id)
        self.client.patch(url, payload)
 
        client.refresh_from_db()
        self.assertEqual(client.user, self.user)
 
    def test_delete_client(self):
        """Test deleting a client successful."""
        client = create_client(user=self.user)
 
        url = detail_url(client.id)
        res = self.client.delete(url)
 
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cliente.objects.filter(id=client.id).exists())
 
    def test_client_other_users_client_error(self):
        """Test trying to delete another users client gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        client = create_client(user=new_user)
 
        url = detail_url(client.id)
        res = self.client.delete(url)
 
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Cliente.objects.filter(id=client.id).exists())