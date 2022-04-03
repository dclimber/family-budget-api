from rest_framework.mixins import DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ..models import Budget
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    BudgetListOutSerializer, BudgetRetrieveCreateDeleteSerializer,
)


class BudgetListCreateDestroyViewSet(
    DestroyModelMixin, ListModelMixin, GenericViewSet
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