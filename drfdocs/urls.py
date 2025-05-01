"""
URL configuration for drfdocs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.exceptions import server_error, bad_request
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from snippets import views

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# handler400 = bad_request     # For 400 Bad Request
# handler500 = server_error    # For 500 Internal Server Error

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
from Apiguide import urls as apiguide_urls
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(router.urls)),
    path('api/', include('quickstart.urls')),
    path('api/', include('Apiguide.urls')),
    # *apiguide_urls.urlpatterns,
    path('', include('snippets.urls')),
    # /api-auth/login/ and /api-auth/logout/ are added by rest_framework.urls by using the SessionAuthentication class in Django REST Framework.
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # path('openapi/', get_schema_view(
    #     title="My Project API",
    #     description="API documentation",
    #     version="1.0.0",
    #     public=True,
    # ), name='openapi-schema'),


     # OpenAPI schema (raw JSON)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc UI
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

# urlpatterns += [
#     # path('api-auth/', include('rest_framework.urls')),
# ]


# urlpatterns = format_suffix_patterns(urlpatterns)
