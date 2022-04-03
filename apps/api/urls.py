from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .v1.urls import urlpatterns as v1_api_patterns

urlpatterns = [
    path('v1/', include(v1_api_patterns)),

    path('schema/', SpectacularAPIView.as_view(), name='open-api-schema'),
    path(
        '',
        SpectacularSwaggerView.as_view(
            url_name='open-api-schema'
        ), name='swagger-ui'
    ),
]
