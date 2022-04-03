import pytest


@pytest.fixture()
def standart_password():
    return 'testpass123'


@pytest.fixture()
def user1(django_user_model, standart_password):
    user = django_user_model.objects.create(
        username='user1',
        first_name='User',
        last_name='Userovich'
    )
    user.set_password(standart_password)
    user.save()
    return user

