import pytest


@pytest.fixture()
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture()
def api_rf():
    from rest_framework.test import APIRequestFactory
    return APIRequestFactory()
