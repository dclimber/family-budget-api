from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ..models import Budget
from .serializers import BudgetListOutSerializer


class BudgetListCreateDestroyViewSet(
    ListModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return BudgetListOutSerializer

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user)
