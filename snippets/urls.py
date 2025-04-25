from django.urls import path
# from .views import snippet_list, snippet_detail
from .views import SnippetList, SnippetDetail
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # Function-based views
    # path('snippets/', snippet_list),
    # path('snippets/<int:pk>/', snippet_detail),

    # Class-based views
    path('snippets/', SnippetList.as_view()),
    path('snippets/<int:pk>/', SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)