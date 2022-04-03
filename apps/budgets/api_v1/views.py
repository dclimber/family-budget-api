from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ..models import Budget, Income
from .permissions import IsOwnerOfBudget, IsOwnerOrReadOnly
from .serializers import (
    BudgetListOutSerializer, BudgetRetrieveCreateDeleteSerializer,
    IncomeRetrieveCreateDeleteSerializer,
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


class UpdateIncomeView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOfBudget]
    serializer_class = IncomeRetrieveCreateDeleteSerializer
    queryset = Income.objects.all().select_related('budget')
