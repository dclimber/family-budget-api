from http import HTTPStatus

import pytest

from django.urls import reverse, reverse_lazy

from ...models import Budget, Expense, ExpenseCategory, Income
from ..views import BudgetListCreateDestroyViewSet


class TestBudgetViewSet:
    url = reverse_lazy('budget-list')

    def create_budget_from_budget_data(
        self, user, budget_data
    ) -> 'Budget':
        budget = Budget.objects.create(name=budget_data['name'], owner=user)
        incomes = [
            Income(
                budget=budget, name=income['name'],
                amount=income['amount']
            ) for income in budget_data['incomes']
        ]
        Income.objects.bulk_create(incomes)
        for category in budget_data['categories']:
            category_obj = ExpenseCategory.objects.create(name=category['name'])
            expenses = [
                Expense(
                    budget=budget, category=category_obj, name=expense['name'],
                    amount=expense['amount']
                ) for expense in category['expenses']
            ]
            Expense.objects.bulk_create(expenses)
        return budget

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

    def test_budget_gets_deleted_correctly(
        self, api_client, user1, budget_data
    ):
        api_client.force_authenticate(user1)
        budget = self.create_budget_from_budget_data(
            user1, budget_data
        )

        response = api_client.delete(
            reverse('budget-detail', args=(budget.id,))
        )

        assert response.status_code == HTTPStatus.NO_CONTENT

        assert Budget.objects.count() == 0
        assert Income.objects.count() == 0
        assert Expense.objects.count() == 0
        assert ExpenseCategory.objects.count() == 0

    @pytest.mark.django_db()
    def test_budget_retrieve_is_in_correct_format(
        self, user1, api_client, budget_data
    ):
        api_client.force_authenticate(user1)
        budget = self.create_budget_from_budget_data(
            user1, budget_data
        )

        response = api_client.get(
            reverse('budget-detail', args=(budget.id,))
        )

        assert response.status_code == HTTPStatus.OK

        json_response = response.json()
        assert 'id' in json_response
        
        assert 'incomes' in json_response
        assert len(json_response['incomes']) == budget.incomes.count()
        income = json_response['incomes'][0]
        assert 'id' in income
        assert 'name' in income
        assert 'amount' in income

        assert 'categories' in json_response
        category = json_response['categories'][0]
        assert 'id' in category
        assert 'name' in category
        assert 'expenses' in category

        expense = category['expenses'][0]
        assert 'id' in expense
        assert 'name' in expense
        assert 'amount' in expense

    @pytest.mark.django_db()
    def test_budget_gets_created(self, user1, api_client, budget_data):
        api_client.force_authenticate(user1)

        response = api_client.post(self.url, data=budget_data, format='json')

        assert response.status_code == HTTPStatus.CREATED

        assert Budget.objects.count() == 1
        budget = Budget.objects.first()
        assert budget.owner == user1
        assert budget.name == budget_data['name']

        assert Income.objects.count() == len(budget_data['incomes'])
        for income in budget_data['incomes']:
            assert Income.objects.filter(
                name=income['name'], amount=income['amount']
            ).exists()

        assert ExpenseCategory.objects.count() == len(
            budget_data['categories']
        )
        for category in budget_data['categories']:
            assert ExpenseCategory.objects.filter(
                name=category['name']
            ).exists()

            category_object = ExpenseCategory.objects.get(name=category['name'])
            
            assert category_object.expenses.count() == len(category['expenses'])
            for expense in category['expenses']:
                assert Expense.objects.filter(
                    name=expense['name'], amount=expense['amount']
                ).exists()
