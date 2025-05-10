from django.test import TestCase

# Create your tests here.
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Docs

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def doc(user):
    return Docs.objects.create(title='Sample Doc', author=user)

@pytest.mark.django_db
def test_list_docs(api_client, doc):
    response = api_client.get('/docs/')
    assert response.status_code == 200
    assert response.data[0]['title'] == 'Sample Doc'

@pytest.mark.django_db
def test_create_doc(api_client, user):
    response = api_client.post('/docs/', {'title': 'New Doc', 'author': user.id}, format='json')
    assert response.status_code == 201
    assert Docs.objects.filter(title='New Doc').exists()

@pytest.mark.django_db
def test_retrieve_doc(api_client, doc):
    response = api_client.get(f'/docs/{doc.id}/')
    assert response.status_code == 200
    assert response.data['title'] == doc.title

@pytest.mark.django_db
def test_update_doc(api_client, doc):
    response = api_client.put(f'/docs/{doc.id}/', {'title': 'Updated Doc', 'author': doc.author.id}, format='json')
    assert response.status_code == 200
    doc.refresh_from_db()
    assert doc.title == 'Updated Doc'

@pytest.mark.django_db
def test_delete_doc(api_client, doc):
    response = api_client.delete(f'/docs/{doc.id}/')
    assert response.status_code == 204
    assert not Docs.objects.filter(id=doc.id).exists()
