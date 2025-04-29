from django.urls import path
from .views import BookList, BookDetail, BookCreateView

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('books/add/', BookCreateView.as_view(), name='book-add'),
]
