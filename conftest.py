from rest_framework_simplejwt.tokens import RefreshToken
from pytest import fixture
from faker import Faker
from pytest_factoryboy import register


from contactsapi.factories import (
    UserFactory, ContactFactory
)

# pytest_plugins = ['contactsapi/conftest']

fake = Faker()

for fact in [
    UserFactory,
    ContactFactory,
]:
    register(fact)

TEST_DATA_RANGE = {'min_value': 50, 'max_value': 80}


@fixture(autouse=True)
def database(db):
    pass


@fixture(scope='function')
def new_user(user_factory):
    user = user_factory.create()
    user.set_password('9874Pass')
    user.save()
    return user


@fixture(scope='function')
def another_user(user_factory):
    user = user_factory.create()
    user.set_password('9tyiYT')
    user.save()
    return user


@fixture(scope='function')
def new_user_no_active(user_factory):
    user = user_factory.create(is_active=False)
    user.set_password('9874Pass')
    user.save()
    return user


@fixture
def headers(new_user):
    token = RefreshToken.for_user(new_user)
    access_token = str(token.access_token)
    return {
        'HTTP_AUTHORIZATION': f'Bearer {access_token}',
        'content_type': 'application/json'
    }


@fixture(scope='module')
def user_data():
    fake = Faker()
    return {
        "password": fake.password(),
        "username": fake.first_name(),
        "email": fake.email()
    }


@fixture(scope='module')
def create_user_data():
    fake = Faker()
    return {
        "password": fake.password(),
        "username": fake.first_name(),
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }


@fixture(scope='function')
def admin_user(admin_factory):
    user = admin_factory.create()
    user.set_password('9874Pass')
    user.save()
    return user


@fixture
def admin_headers(admin_user):
    token = RefreshToken.for_user(admin_user)
    access_token = str(token.access_token)
    return {
        'HTTP_AUTHORIZATION': f'Bearer {access_token}',
        'content_type': 'application/json'
    }


@fixture
def new_user_contact(new_user, contact_factory):
    contact = contact_factory.create(owner=new_user)
    return contact
