from rest_framework import serializers

from ..models import Budget


class BudgetListOutSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'id')
        model = Budget
