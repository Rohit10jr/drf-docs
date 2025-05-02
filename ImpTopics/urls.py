from django.urls import path
from .views import UserList, BlogListView, BlogDetailView, BlogCreate, ArticleListView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, ArticleFullView # PostListCreateView, PostRetrieveDeleteView
from .serializers import UserSerializer
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.models import User
from .views import  GenericArticleListView, GenericArticleCreateView,  GenericArticleDetailView, GenericArticleUpdateView, GenericArticleDeleteView, GenericListCreateView, GenericRetrieveUpdateDeleteView, OneViewForAll, RetrieveOrderView

urlpatterns = [
    path('listuser/', UserList.as_view()), 
    path('listurl/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list'),
    path('blog/', BlogListView.as_view(), name='book-list'),
    path('blog/<slug:book_slug>/', BlogDetailView.as_view(), name='book-detail'),
    path('blogcreate/', BlogCreate.as_view(), name='book-create'),
    # path('post/', PostListCreateView.as_view(), name='post-create'),
    # path('posts/<int:pk>/', PostRetrieveDeleteView.as_view(), name='post-detail-delete'),
    # path('articles/', ArticleListView.as_view(), name='article-list'),
    # path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
    # path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    # path('articles/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    # path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),

    # path('articlesfull/', ArticleFullView.as_view(), name='article-list-create'),
    # path('articlesfull/<int:id>/', ArticleFullView.as_view(), name='article-detail-update-delete'),

    # GENERIC VIEWS URL
    # GET all articles, 
    path('articles/', GenericArticleListView.as_view(), name='article-list'),
    # POST new article
    path('articles/create/', GenericArticleCreateView.as_view(), name='article-create'),

    # Retrieve one article (GET)
    path('articles/<int:pk>/view/', GenericArticleDetailView.as_view(), name='article-retrieve'),

    # Update one article (PUT/PATCH)
    path('articles/<int:pk>/update/',GenericArticleUpdateView.as_view(), name='article-update'),

    # Delete one article (DELETE)
    path('articles/<int:pk>/delete/', GenericArticleDeleteView.as_view(), name='article-delete'),

    # Or use this single path instead of the above 3:
    # GET, PUT/PATCH, DELETE all in one
    path('articlesLC/', GenericListCreateView.as_view(), name='article-LC'),
    path('articlesRUD/<int:pk>/', GenericRetrieveUpdateDeleteView.as_view(), name='article-RUD'),
    path('one4allCrud/', OneViewForAll.as_view(), name='article-CR'),
    path('one4allCrud/<int:pk>/', OneViewForAll.as_view(), name='article-RUD'),

    # urls.py
    path('orders/<int:customer_id>/<str:order_number>/', RetrieveOrderView.as_view())

]
