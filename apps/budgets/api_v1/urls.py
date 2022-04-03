from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BudgetListCreateDestroyViewSet, ExpenseCategoryCRUDViewSet,
    IncomeCreateUpdateDestroyViewSet,
)

router = DefaultRouter()
router.register('', BudgetListCreateDestroyViewSet, basename='budget')
router.register('incomes', IncomeCreateUpdateDestroyViewSet, basename='income')
router.register(
    'categories', ExpenseCategoryCRUDViewSet, basename='category'
)

urlpatterns = [
    path('', include(router.urls)),
]
