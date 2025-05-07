from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, UserProfileViewset, UserProfileApiview,UserProfileDetailAPIView , NovelRetrieveUpdateDestroyView, NovelListCreateView, DataPointColorListCreateView, DataPointColorDetailView

urlpatterns = [
    # For CBV
    # path('comments/', views.CommentListCreateAPIView.as_view(), name='comment-list-create'),
    # path('comments/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),

    # Uncomment for FBV
    path('comments/', views.comment_list_create, name='comment-list-create'),
    path('comments/<int:pk>/', views.comment_detail, name='comment-detail'),
     path('temppost/', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('temppost/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('news/', views.NewsListCreateView.as_view(), name='news-list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/bulk-update/', views.BookBulkUpdateView.as_view(), name='book-bulk-update'),
    path('userpro/', UserProfileApiview.as_view(), name='userPro'),
    path('userpro/<int:pk>/', UserProfileDetailAPIView.as_view(), name='userPro'),
    path('novel/', NovelListCreateView.as_view(), name='novel-list-create'),
    path('novel/<int:pk>/', NovelRetrieveUpdateDestroyView.as_view(), name='novel-detail'),
    path('color/', DataPointColorListCreateView.as_view(), name='color'),
    path('color/', DataPointColorDetailView.as_view(), name='color'),
]


router = DefaultRouter()

# router.register(r'accounts', AccountViewSet)
# router.register(r'userprofile', UserProfileViewset)
# urlpatterns += [
#     path('', include(router.urls)),
# ]