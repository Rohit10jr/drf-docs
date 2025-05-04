from django.urls import path, include
from .views import BookList, BookDetail, BookCreateView, BookCreateViewApi, BookCreateViewApi
from .views import BookList, BookDetail, BookCreateView, BookCreateViewApi, BookCreateViewApi, GlobalMetadataView, PerViewMetadataView, SchemaViewSet, MinimalExampleView, NoNegotiationView, CommentList
from rest_framework.routers import DefaultRouter
from .views import SchemaViewSet, ProductListCreateView, ProductListView, HelloView, DefaultVersionAPI, QueryVersionAPI, RequestInspectorView, hello_world, hello_world_2, hello_world_3, ListUsers,schema_view, schema_view_2, greet_user, EchoView, UserCountView, user_count_view, ProductDetailHTMLView, static_html_view, ProductJSONView, ProductListRenderView, ContactView, ProductPlainTextView, ProductDetailRenderView, MyProductListView, ProductAdminView, list_users
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
    path('defaultversion/', DefaultVersionAPI.as_view(), name='version'),
    path('queryversion/', QueryVersionAPI.as_view(), name='version'),
    path('requestInspection/', RequestInspectorView.as_view(), name='version'),

    path('hello1/', hello_world),
    path('hello2/', hello_world_2),
    path('hello3/', hello_world_3),
    path('schema/', schema_view),
    path('schema2/', schema_view_2),
    path('greetuser/', greet_user),
    path('echo/', EchoView.as_view()),
    path('listusers/', ListUsers.as_view()),
    path('countusers/', UserCountView.as_view()),
    path('countusers2/', user_count_view),
    path('jsonresponse/<int:pk>/', ProductJSONView.as_view()),
    path('jsonresponse/', ProductJSONView.as_view()),
    path('htmlresponse/<int:pk>/', ProductDetailHTMLView.as_view()),
    path('htmlresponse/', ProductDetailHTMLView.as_view()),
    # path('htmlresponse/', ProductListRenderView.as_view()),
    # path('htmlresponse/<int:pk>/', ProductDetailRenderView.as_view()),
    path('staticresponse/', static_html_view),
    path('custom1/', MyProductListView.as_view()),
    path('custom2/', ProductAdminView.as_view()),
    path('custom3/', ContactView.as_view()),
    path('custom4/<int:pk>/', ProductPlainTextView.as_view()),
    path('list_users/', list_users),

]

# router = DefaultRouter()
# router.register(r'schema', SchemaViewSet, basename='schema')

# urlpatterns += [
#     path('', include(router.urls)),
# ]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
