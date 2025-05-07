from django.urls import path
from .views import UserList, BlogListView, BlogDetailView, BlogCreate, ArticleListView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, ArticleFullView # PostListCreateView, PostRetrieveDeleteView
from .serializers import UserSerializer
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.models import User
from .views import  GenericArticleListView, GenericArticleCreateView,  GenericArticleDetailView, GenericArticleUpdateView, GenericArticleDeleteView, GenericListCreateView, GenericRetrieveUpdateDeleteView, OneViewForAll, RetrieveOrderView, ArticleGenericViewSet, UserActionViewSet, BlogCacheView, get_user_name, ProfileViewCache, UserFeedView, example_throttle_view, ExampleThrottleView, custom_example_throttle_view, custom_view,MyThrottledView, PostListView, CommentView, LikeView, PurchaseList, PurchaseListByUsername, PurchaseListWithQueryParam, ProductListFilterView, UserSerachListView, UserOrderListView, ProductFilterSearchOrderView

from .views import UserViewSet, UserModelViewSet, ArticleViewSet, ArticleModelViewSet, ArticleReadOnlyViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('listuser/', UserList.as_view()), 
    path('listurl/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list'),
    path('blog/', BlogListView.as_view(), name='book-list'),
    path('blog/<slug:book_slug>/', BlogDetailView.as_view(), name='book-detail'),
    path('blogcreate/', BlogCreate.as_view(), name='book-create'),
    # path('post/', PostListCreateView.as_view(), name='post-create'),
    # path('posts/<int:pk>/', PostRetrieveDeleteView.as_view(), name='post-detail-delete'),
    # path('posts/<slug:slug>/', PostRetrieveDeleteView.as_view(), name='post-detail-delete'),
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
    path('orders/<int:customer_id>/<str:order_number>/', RetrieveOrderView.as_view()),
    path('usercache/', get_user_name),
    path('user2cache/', BlogCacheView.as_view()),
    path('user3cache/', ProfileViewCache.as_view({'get': 'list'})),
    path('user4cache/', UserFeedView.as_view()), 
    path('throttle/', example_throttle_view), 
    path('throttle2/', ExampleThrottleView.as_view()), 
    path('throttle3/', custom_example_throttle_view), 
    path('throttle4/', custom_view),
    path('throttle/', MyThrottledView.as_view()),
    path('throttlepost/', PostListView.as_view(), name='post-list'),
    path('throttlecomments/', CommentView.as_view(), name='comment'),
    path('throttlelikes/', LikeView.as_view(), name='like'),
    path('purchase1/', PurchaseList.as_view(), name='PurchaseList'),
    path('purchase2/<str:username>/', PurchaseListByUsername.as_view()),
    path('purchase3/', PurchaseListWithQueryParam.as_view()),
    path('filterproduct/', ProductListFilterView.as_view()),
    path('searchuser/', UserSerachListView.as_view()),
    path('orderuser/', UserOrderListView.as_view()),
    path('productfso/', ProductFilterSearchOrderView.as_view()),

]

router = DefaultRouter()
# router.register(r'userviewset', UserViewSet, basename='user')
router.register(r'userviewset', UserModelViewSet, basename='user')
router.register(r'useraction', UserActionViewSet, basename='useraction')
router.register(r'articleviewset', ArticleViewSet, basename='article')
router.register(r'articlemodel', ArticleModelViewSet, basename='articlemodel')
router.register(r'articlegerneric', ArticleGenericViewSet, basename='articlegeneric')
router.register(r'articlereadonly', ArticleReadOnlyViewSet, basename='articlemodelreadonly')

urlpatterns += router.urls