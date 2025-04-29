from django.urls import path, include
from .views import BookList, BookDetail, BookCreateView, BookCreateViewApi, BookCreateViewApi
from .views import BookList, BookDetail, BookCreateView, BookCreateViewApi, BookCreateViewApi, GlobalMetadataView, PerViewMetadataView, SchemaViewSet, MinimalExampleView
from rest_framework.routers import DefaultRouter
from .views import SchemaViewSet

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('booksapi/', BookCreateViewApi.as_view(), name='book-add-api'),
    path('books/add/', BookCreateView.as_view(), name='book-add'),
    path('metadata/', GlobalMetadataView.as_view(), name='meta-data'),
    path('preview/', PerViewMetadataView.as_view(), name='preview-data'),
    path('minimal/', MinimalExampleView.as_view()),
]

router = DefaultRouter()
router.register(r'schema', SchemaViewSet, basename='schema')

urlpatterns += [
    path('', include(router.urls)),
]
