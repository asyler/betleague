import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from factory import lazy_attribute


class _UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')


class UserFactory(object):
    @classmethod
    def create(cls, **kwargs):
        user = _UserFactory.create(**kwargs)
        password = user.password
        user.set_password(password)
        user.save()
        user.raw_password = password
        return user