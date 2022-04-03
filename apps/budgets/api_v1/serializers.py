from rest_framework import serializers

from ..models import Budget, Expense, ExpenseCategory, Income


class BudgetListOutSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'id')
        model = Budget


class IncomeRetrieveCreateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('id', 'name', 'amount')


class ExpenseRetrieveCreateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'name', 'amount')


class ExpenseCategoryRetrieveCreateDeleteSerializer(
    serializers.ModelSerializer
):
    expenses = ExpenseRetrieveCreateDeleteSerializer(many=True)

    class Meta:
        model = ExpenseCategory
        fields = ('id', 'name', 'expenses')


class BudgetRetrieveCreateDeleteSerializer(serializers.ModelSerializer):
    incomes = IncomeRetrieveCreateDeleteSerializer(many=True)
    categories = ExpenseCategoryRetrieveCreateDeleteSerializer(many=True)

    class Meta:
        fields = (
            'id', 'name', 'incomes', 'categories',
        )
        model = Budget
