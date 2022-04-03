from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BudgetListCreateDestroyViewSet, UpdateIncomeView

router = DefaultRouter()
router.register('', BudgetListCreateDestroyViewSet, basename='budget')

urlpatterns = [
    path('incomes/<uuid:pk>', UpdateIncomeView.as_view(), name='update-income'),
    path('', include(router.urls)),
]
