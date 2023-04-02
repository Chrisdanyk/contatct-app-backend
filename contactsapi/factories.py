import factory
from faker import Faker
from contact.models import Contact
from authentication.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    is_active = True


class AdminFactory(UserFactory):
    email = "admin@tiktik.nl"
    is_superuser = True
    is_staff = True
    is_admin = True


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    country_code = fake.word()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone_number = fake.phone_number()
