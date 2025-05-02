from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer, BlogSerializer,PostSerializer, PostReadOnlySerializer, ArticleSerializer, OrderSerializer
from rest_framework import generics 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
# Create your views here.
from .models import Blog, Post, Article, Order
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework import serializers
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin,
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView,
    UpdateAPIView, DestroyAPIView, ListCreateAPIView,
    RetrieveUpdateAPIView, RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView
)

from .mixins import MultipleFieldLookupMixin

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


    # def list(self, request):
    #     queryset = self.get_queryset()
    #     print("queryset", queryset)
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)
    

class BlogPagination(PageNumberPagination):
    page_size = 5


class BlogCreate(CreateModelMixin, GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BlogListView(ListModelMixin, GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class BlogDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'Blog_slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    

# class PostListCreateView(ListCreateAPIView):
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # return super().get_queryset()
#         return Post.objects.filter(user=self.request.user)

#     def get_serializer_class(self):
#         # Admins get full detail, others get limited
#         if self.request.user.is_staff:
#             return PostSerializer
#         return PostReadOnlySerializer

#     def perform_create(self, serializer):
#         # Prevent duplicate titles for same user
#         if Post.objects.filter(user=self.request.user, title=serializer.validated_data['title']).exists():
#             raise serializers.ValidationError("You already created a post with this title.")
#         serializer.save(user=self.request.user)

# class PostRetrieveDeleteView(RetrieveDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'pk'  # or 'slug' or other field if needed

#     def get_queryset(self):
#         # Only return posts belonging to the current user
#         return Post.objects.filter(user=self.request.user)

#     def get_serializer_class(self):
#         # Admins see full serializer, others see read-only
#         if self.request.user.is_staff:
#             return PostSerializer
#         return PostReadOnlySerializer

#     def perform_destroy(self, instance):
#         # Example: prevent deletion if post is marked "protected"
#         if getattr(instance, 'is_protected', False):
#             raise serializers.ValidationError("You cannot delete a protected post.")
#         instance.delete()



# different mixins 

class ArticleListView(ListModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ArticleCreateView(CreateModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class ArticleDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    

class ArticleUpdateView(UpdateModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    

class ArticleDeleteView(DestroyModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
# everything together
class ArticleFullView(ListModelMixin,
                      CreateModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



# concrete generic views


class GenericArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class GenericArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


# Read One (GET)
class GenericArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

# Update One (PUT/PATCH)
class GenericArticleUpdateView(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

# Delete One (DELETE)
class GenericArticleDeleteView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

# Read All (GET), Create (POST)
class GenericListCreateView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Full Read-Update-Delete (GET, PUT/PATCH, DELETE)
class GenericRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'


class OneViewForAll(ListCreateAPIView,RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'


# custom multiple url field views in mixins 
class BaseRetrieveView(MultipleFieldLookupMixin, RetrieveAPIView):
    pass

class RetrieveOrderView(BaseRetrieveView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_fields = ['customer_id', 'order_number']
