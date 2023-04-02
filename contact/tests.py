
from rest_framework import status
from contact.models import Contact


def test_create_contact_with_no_auth(client):
    sample_contact = {
        'first_name': 'john',
        'last_name': 'doe',
        'phone_number': '99999999',
        'country_code': '001',
    }
    response = client.post('/api/contacts/', data=sample_contact)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_contact(client, headers):
    sample_contact = {
        'first_name': 'john',
        'last_name': 'doe',
        'phone_number': '99999999',
        'country_code': '001',
    }
    previous_contact_count = Contact.objects.count()
    response = client.post('/api/contacts/',
                           data=sample_contact, **headers)
    assert Contact.objects.count() == previous_contact_count + 1
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['first_name'] == 'john'


def test_update_contact(client, headers, new_user_contact):
    response = client.put(f'/api/contacts/{new_user_contact.id}',
                          data={"first_name": "xis"}, **headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['data']['first_name'] == 'xis'


def test_get_contact(client, headers, new_user_contact):
    response = client.get(f'/api/contacts/{new_user_contact.id}',
                          **headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['data']['first_name'] == new_user_contact.first_name


def test_get_unexisting_contact(client, headers, new_user_contact):
    response = client.get('/api/contacts/777', **headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_retrieve_all_owners_contacts(client, new_user_contact, headers):
    response = client.get('/api/contacts/', **headers)
    assert isinstance(response.data['results'], list)
    assert len(response.data['results']) > 0
    assert isinstance(response.data['count'], int)
    assert response.status_code == status.HTTP_200_OK
