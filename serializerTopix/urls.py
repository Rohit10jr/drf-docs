from django.urls import path
from . import views

urlpatterns = [
    # For CBV
    # path('comments/', views.CommentListCreateAPIView.as_view(), name='comment-list-create'),
    # path('comments/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),

    # Uncomment for FBV
    path('comments/', views.comment_list_create, name='comment-list-create'),
    path('comments/<int:pk>/', views.comment_detail, name='comment-detail'),
     path('temppost/', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('temppost/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),

]