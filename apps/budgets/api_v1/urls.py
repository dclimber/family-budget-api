from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BudgetListCreateDestroyViewSet

router = DefaultRouter()
router.register('', BudgetListCreateDestroyViewSet, basename='budget')

urlpatterns = [
    path('', include(router.urls)),
]
