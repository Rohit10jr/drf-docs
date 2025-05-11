from django.test import TestCase

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Docs, BillingRecord
from rest_framework.authtoken.models import Token

# from django.urls import reverse
from rest_framework.reverse import reverse 
from rest_framework import status
from datetime import date
from decimal import Decimal


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def doc(user):
    return Docs.objects.create(title='Sample Doc', author=user)

@pytest.fixture
def user(db):
    user = User.objects.create_user(
        id=1, username='rohit100', password='1234'
    )
    return user

@pytest.fixture
def auth_client(api_client, user):
    api_client.login(username='rohit100', password='1234')
    return api_client

# ---------- Test Cases for docs model----------

@pytest.mark.django_db
def test_create_doc(auth_client, user):
    data = {
        'title': 'Test Document',
        'author': user.id
    }
    response = auth_client.post('/api/testdocs/', data, format='json')
    assert response.status_code == 201
    assert Docs.objects.filter(title='Test Document').exists()

@pytest.mark.django_db
def test_list_docs(auth_client, doc):
    response = auth_client.get('/api/testdocs/')
    assert response.status_code == 200
    assert any(d['title'] == 'Sample Doc' for d in response.data['results'])
    # assert any(d['title'] == 'Existing Doc' for d in response.data['results'])

@pytest.mark.django_db
def test_retrieve_doc(auth_client, doc):
    response = auth_client.get(f'/api/testdocs/{doc.id}/')
    assert response.status_code == 200
    # assert response.data['title'] == 'Existing Doc'
    assert response.data['title'] == 'Sample Doc'


@pytest.mark.django_db
def test_update_doc(auth_client, doc):
    updated_data = {
        'title': 'Updated Title',
        'author': doc.author.id
    }
    response = auth_client.put(f'/api/testdocs/{doc.id}/', updated_data, format='json')
    assert response.status_code == 200
    doc.refresh_from_db()
    assert doc.title == 'Updated Title'

@pytest.mark.django_db
def test_delete_doc(auth_client, doc):
    response = auth_client.delete(f'/api/testdocs/{doc.id}/')
    assert response.status_code == 204
    assert not Docs.objects.filter(id=doc.id).exists()


# ---------- Test Cases for billing model----------

@pytest.mark.django_db
def test_create_billing_record(api_client):
    url = '/api/billing/'
    payload = {
        'client': 'Acme Corp',
        'date': '2024-05-01',
        'amount': '1999.99'
    }
    #     url = reverse('billing-list')  # from router
    #     payload = {
    #         'client': 'Acme Corp',
    #         'date': '2024-05-01',
    #         'amount': '1999.99'
    #     }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert BillingRecord.objects.count() == 1
    assert BillingRecord.objects.first().client == 'Acme Corp'


@pytest.mark.django_db
def test_list_billing_records(api_client):
    BillingRecord.objects.create(client="Client A", date="2024-01-01", amount=100.00)
    BillingRecord.objects.create(client="Client B", date="2024-01-02", amount=200.00)

    url = '/api/billing/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2  # If pagination is enabled


@pytest.mark.django_db
def test_retrieve_billing_record(api_client):
    record = BillingRecord.objects.create(client="Client A", date="2024-01-01", amount=100.00)
    url = f'/api/billing/{record.id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['client'] == 'Client A'


@pytest.mark.django_db
def test_update_billing_record(api_client):
    record = BillingRecord.objects.create(client="Client A", date="2024-01-01", amount=100.00)
    url = f'/api/billing/{record.id}/'
    payload = {
        'client': 'Client Updated',
        'date': '2024-01-01',
        'amount': '150.00'
    }
    response = api_client.put(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    record.refresh_from_db()
    assert record.client == 'Client Updated'
    assert record.amount == Decimal('150.00')


@pytest.mark.django_db
def test_delete_billing_record(api_client):
    record = BillingRecord.objects.create(client="Client A", date="2024-01-01", amount=100.00)
    url = f'/api/billing/{record.id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert BillingRecord.objects.count() == 0
