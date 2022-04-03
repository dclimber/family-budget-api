from decimal import Decimal

from ..models import Budget, Expense, ExpenseCategory, Income


def test_budgets_models_have_correct_str_method(user1):
    budget = Budget(owner=user1, name='test')
    budget_str = f'Budget "{budget.name}"'
    budget_income = Income(
        name='test', budget=budget, amount=Decimal(10)
    )
    budget_income_str = f'Income "{budget_income.name}" for {budget_str}'
    expense_category = ExpenseCategory(
        name='test'
    )
    expense_category_str = f'Expense category: {expense_category.name}'
    expense = Expense(
        budget=budget, category=expense_category, name='rent',
        amount=Decimal(1000)
    )
    expense_str = f'Expense "{expense.name}" for {budget}'
    cases = (
        (budget, budget_str),
        (budget_income, budget_income_str),
        (expense_category, expense_category_str),
        (expense, expense_str)
    )

    for obj, result in cases:
        assert str(obj) == result
