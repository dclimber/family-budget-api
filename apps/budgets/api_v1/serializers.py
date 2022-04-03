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

    def create(self, validated_data):
        incomes_data = validated_data.pop('incomes')
        expenses_by_category = validated_data.pop('categories')
        budget = Budget.objects.create(**validated_data)
        incomes = [
            Income(
                budget=budget,
                **income
            ) for income in incomes_data
        ]
        Income.objects.bulk_create(incomes)
        expenses = []
        for category in expenses_by_category:
            name = category['name']
            category_obj, _ = ExpenseCategory.objects.get_or_create(name=name)
            expenses += [
                Expense(
                    budget=budget,
                    name=expense['name'],
                    amount=expense['amount'],
                    category = category_obj
                ) for expense in category['expenses']
            ]
        Expense.objects.bulk_create(expenses)
        return budget


class IncomeCreateDeleteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'budget', 'name', 'amount')
        model = Income
