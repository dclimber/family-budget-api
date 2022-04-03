from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='open-api-schema'),
    path(
        '',
        SpectacularSwaggerView.as_view(
            url_name='open-api-schema'
        ), name='swagger-ui'
    ),
]
