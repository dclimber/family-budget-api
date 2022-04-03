from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ..models import Budget, Expense, ExpenseCategory, Income
from .permissions import IsOwnerOfBudget, IsOwnerOrReadOnly
from .serializers import (
    BudgetListOutSerializer, BudgetRetrieveCreateDeleteSerializer,
    ExpenseCategoryCRUDSerializer, ExpenseCRUDSerializer,
    IncomeCreateDeleteUpdateSerializer,
)


class BudgetListCreateDestroyViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, 
    RetrieveModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return BudgetListOutSerializer
        return BudgetRetrieveCreateDeleteSerializer

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        categories = list(instance.categories.all().distinct())
        super().perform_destroy(instance)
        # delete categories with no expenses
        for category in categories:
            if not category.expenses.exists():
                category.delete()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IncomeCreateUpdateDestroyViewSet(
    CreateModelMixin, DestroyModelMixin, 
    UpdateModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated, IsOwnerOfBudget]
    queryset = Income.objects.all().select_related('budget')
    serializer_class = IncomeCreateDeleteUpdateSerializer


class ExpenseCategoryCRUDViewSet(
    CreateModelMixin, DestroyModelMixin, RetrieveModelMixin,
    UpdateModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategoryCRUDSerializer


class ExpenseCRUDViewSet(
    CreateModelMixin, DestroyModelMixin, RetrieveModelMixin,
    UpdateModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated, IsOwnerOfBudget]
    queryset = Expense.objects.all().select_related('budget', 'category')
    serializer_class = ExpenseCRUDSerializer
