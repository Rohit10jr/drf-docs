from django.urls import path
from .views import snippet_list, snippet_detail
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('snippets/', snippet_list),
    path('snippets/<int:pk>/', snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)