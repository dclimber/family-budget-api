from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BudgetListCreateDestroyViewSet, IncomeCreateUpdateDestroyViewSet,
)

router = DefaultRouter()
router.register('', BudgetListCreateDestroyViewSet, basename='budget')
router.register('incomes', IncomeCreateUpdateDestroyViewSet, basename='income')

urlpatterns = [
    path('', include(router.urls)),
]
