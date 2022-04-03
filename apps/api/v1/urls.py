from django.urls import include, path

from apps.budgets.api_v1 import urls as budget_urls

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('budgets/', include(budget_urls))
]
