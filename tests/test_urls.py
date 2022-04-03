from http import HTTPStatus

from django.urls import resolve


def test_api_root_page_is_swagger(client):
    path = '/api/'
    name = 'swagger-ui'

    response = client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert resolve(path).url_name == name


def test_django_admin_is_available(admin_client):
    path = '/admin/'
    response = admin_client.get(path)

    found_func = resolve(path)

    assert response.status_code == HTTPStatus.OK
    assert found_func.url_name == 'index'
    assert found_func.app_name == 'admin'
