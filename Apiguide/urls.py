from django.urls import path, include
from .views import BookList, BookDetail, BookCreateView, BookCreateViewApi, BookCreateViewApi
from .views import BookList, BookDetail, BookCreateView, BookCreateViewApi, BookCreateViewApi, GlobalMetadataView, PerViewMetadataView, SchemaViewSet, MinimalExampleView, NoNegotiationView, CommentList
from rest_framework.routers import DefaultRouter
from .views import SchemaViewSet, ProductListCreateView, ProductListView, HelloView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('bookss/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    # path('booksapi/', BookCreateViewApi.as_view(), name='book-add-api'),
    path('books/add/', BookCreateView.as_view(), name='book-add'),
    path('metadata/', GlobalMetadataView.as_view(), name='meta-data'),
    path('preview/', PerViewMetadataView.as_view(), name='preview-data'),
    path('minimal/', MinimalExampleView.as_view()),
    path('no-negotiation/', NoNegotiationView.as_view()),
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('pagedefault/', ProductListCreateView.as_view(), name='product-list-create'),
    path('pagecustom/', ProductListView.as_view(), name='product-list-create'),
    path('HelloView/', HelloView.as_view(), name='HelloView'),

]

# router = DefaultRouter()
# router.register(r'schema', SchemaViewSet, basename='schema')

# urlpatterns += [
#     path('', include(router.urls)),
# ]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
