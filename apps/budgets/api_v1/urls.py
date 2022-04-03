from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BudgetListCreateDestroyViewSet, ExpenseCategoryCRUDViewSet,
    ExpenseCRUDViewSet, IncomeCreateUpdateDestroyViewSet,
)

router = DefaultRouter()
router.register('', BudgetListCreateDestroyViewSet, basename='budget')
router.register('incomes', IncomeCreateUpdateDestroyViewSet, basename='income')
router.register(
    'categories', ExpenseCategoryCRUDViewSet, basename='category'
)
router.register(
    'expenses', ExpenseCRUDViewSet, basename='expense'
)

urlpatterns = [
    path('', include(router.urls)),
]
