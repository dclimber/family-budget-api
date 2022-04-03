from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BudgetListCreateDestroyViewSet, CreateUpdateDestroyIncomeViewSet,
)

router = DefaultRouter()
router.register('', BudgetListCreateDestroyViewSet, basename='budget')
router.register('incomes', CreateUpdateDestroyIncomeViewSet, basename='income')

urlpatterns = [
    path('', include(router.urls)),
]
