import pytest


@pytest.fixture()
def budget_data():
    return {
        'name': 'test-budget',
        'incomes': [
            {
                'name': 'test-income',
                'amount': '200.00'
            },
            {
                'name': 'test-income 2',
                'amount': '1000.00'
            }
        ],
        'categories': [
            {
                'name': 'utilities',
                'expenses': [
                    {
                        'name': 'internet',
                        'amount': '20.00'
                    },
                ]
            },
            {
                'name': 'food',
                'expenses': [
                    {
                        'name': 'meat',
                        'amount': '30.00'
                    },
                    {
                        'name': 'dairy',
                        'amount': '20.00'
                    },
                ]
            }
        ]
    }
