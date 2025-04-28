from django.urls import path
# from .t snippet_list, snippet_detail
from .views import SnippetList, SnippetDetail, UserList, UserDetail, api_root, SnippetHighlight
from rest_framework.urlpatterns import format_suffix_patterns


# urlpatterns = [
#     # Function-based views
#     # path('snippets/', snippet_list),
#     # path('snippets/<int:pk>/', snippet_detail),

#     # Class-based views
#     path('snippets/', SnippetList.as_view()),
#     path('snippets/<int:pk>/', SnippetDetail.as_view()),
#     path('users/', UserList.as_view()),
#     path('users/<int:pk>/', UserDetail.as_view()),
#     path('', api_root), 
#     path('snippets/<int:pk>/hightlight/', SnippetHighlight.as_view())
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

# urlpatterns = format_suffix_patterns([
#     path('', api_root),
#     path('snippets/',
#         SnippetList.as_view(),
#         name='snippet-list'),
#     path('snippets/<int:pk>/',
#         SnippetDetail.as_view(),
#         name='snippet-detail'),
#     path('snippets/<int:pk>/highlight/',
#         SnippetHighlight.as_view(),
#         name='snippet-highlight'),
#     path('users/',
#         UserList.as_view(),
#         name='user-list'),
#     path('users/<int:pk>/',
#         UserDetail.as_view(),
#         name='user-detail')
# ])


from rest_framework import renderers

from .views import api_root, SnippetViewSet, UserViewSet


# Binding ViewSets to URLs explicitly

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})


urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])

# Using Routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from snippets import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns +=[path('openapi/', get_schema_view(
        title="My API",
        description="API for all endpoints",
        version="1.0.0"
    ), name='openapi-schema'),]