from http import HTTPStatus

import pytest

from django.urls import reverse_lazy

from ...models import Budget
from ..views import BudgetListCreateDestroyViewSet


class TestBudgetViewSet:
    url = reverse_lazy('budget-list')

    def test_non_authenticated_users_dont_have_access(
        self, api_client
    ):
        response = api_client.get(self.url)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_get_queryset_returns_budgets_of_the_authenticated_user(
        self, user1, user2, api_rf
    ):
        user1_budgets = [
            Budget(owner=user1, name=f'budget of {user1.username} {num}')
            for num in range(10)
        ]
        user2_budgets = [
            Budget(owner=user2, name=f'budget of {user2.username} {num}')
            for num in range(5)
        ]
        Budget.objects.bulk_create(user1_budgets + user2_budgets)

        request = api_rf.get(self.url)
        request.user = user1
        view = BudgetListCreateDestroyViewSet()
        view.setup(request)
        queryset = view.get_queryset()

        assert queryset.count() == len(user1_budgets)
        assert queryset.exclude(owner=user1).count() == 0

    @pytest.mark.django_db()
    def test_budget_list_is_in_correct_format(
        self, user1, api_client, settings
    ):
        budget_count = settings.PAGE_SIZE * 4 + 2
        page_num = 2
        api_client.force_authenticate(user1)
        budget_name_prefix = 'test '
        budgets = [
            Budget(owner=user1, name=f'{budget_name_prefix}{num}')
            for num in range(budget_count)
        ]
        Budget.objects.bulk_create(budgets)

        response = api_client.get(self.url, {'page': page_num})

        assert response.status_code == HTTPStatus.OK
        json_response = response.json()

        # make sure paginator works
        assert 'count' in json_response
        assert json_response['count'] == budget_count
        assert 'next' in json_response
        assert 'previous' in json_response

        # check budgets
        assert 'results' in json_response
        budget = json_response['results'][0]
        assert 'name' in budget
        assert 'id' in budget
        assert budget_name_prefix in budget['name']
