from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BudgetListCreateDestroyViewSet, ExpenseCategoryCRUDViewSet,
    ExpenseCRUDViewSet, IncomeCRUDViewSet,
)

router = DefaultRouter()
router.register('', BudgetListCreateDestroyViewSet, basename='budget')
router.register('incomes', IncomeCRUDViewSet, basename='income')
router.register(
    'categories', ExpenseCategoryCRUDViewSet, basename='category'
)
router.register(
    'expenses', ExpenseCRUDViewSet, basename='expense'
)

urlpatterns = [
    path('', include(router.urls)),
]
