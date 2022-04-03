from http import HTTPStatus

import pytest
import requests


@pytest.fixture()
def users_data(standart_password):
    num_users = 3
    users_data = [
        {
            'username': f'testuser{num}',
            'password': standart_password,
            'email': f'test{num}@test.com'
        } for num in range(num_users)
    ]
    return users_data


class TestLiveV1API:
    """Some functional tests for the app."""
    token_prefix = 'Bearer'
    auth_header = 'AUTHORIZATION'

    def test_users_can_signup_and_create_budgets(
        self, users_data, live_server,
    ):
        # The application should allow for creating several users.
        for data in users_data:
            response = requests.post(
                f'{live_server.url}/api/v1/auth/users/',
                data=data,
            )

            assert response.status_code == HTTPStatus.CREATED

        # Users can login and access api.
        for user in users_data:
            # authenticate user
            response = requests.post(
                f'{live_server.url}/api/v1/auth/jwt/create/',
                data=dict(username=user['username'], password=user['password'])
            )

            assert response.status_code == HTTPStatus.OK
            assert 'access' in response.json()

            access_token = response.json()['access']

            jwt_token: str = f'{self.token_prefix} {access_token}'
            response = requests.get(
                f'{live_server.url}/api/v1/auth/users/me/',
                headers={self.auth_header: jwt_token}
            )

            assert response.status_code == HTTPStatus.OK
            json_response = response.json()
            assert 'email' in json_response
            assert 'id' in json_response
            assert 'username' in json_response
