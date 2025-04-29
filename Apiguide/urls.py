from django.urls import path
from .views import BookList, BookDetail, BookCreateView, BookCreateViewApi, BookCreateViewApi
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('booksapi/', BookCreateViewApi.as_view(), name='book-add-api'),
    path('books/add/', BookCreateView.as_view(), name='book-add'),
]
