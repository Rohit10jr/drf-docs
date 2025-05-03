from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer, BlogSerializer,PostSerializer, PostReadOnlySerializer, ArticleSerializer, OrderSerializer, PasswordSerializer
from rest_framework import generics 
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
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

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from rest_framework import viewsets, mixins
from rest_framework.response import Response


from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer, CharField
from rest_framework.decorators import action


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


# view sets 

############ Different types of viewsets ############

# ✅ 1. ViewSet (manual implementations)
class ArticleViewSet(viewsets.ViewSet):
    """
    A custom ViewSet with all standard actions and conditional permissions.
    """
    def get_permissions(self):
        """
        Return permission classes based on action.
        """
        print("1 one")
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        print("2 two")
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=HTTP_200_OK)

    def update(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    def partial_update(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    def destroy(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# ✅ 2. ModelViewSet (full CRUD support)
class ArticleModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Article instances.
    Includes custom permissions based on action.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        """
        Set permissions based on action.
        Only authenticated users can list,
        but only admins can create, update, or delete.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


# ✅ 3. GenericViewSet / Custom ViewSet (requires mixins)
class ArticleGenericViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    GenericViewSet with mixins.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


# ✅ 4. ReadOnlyModelViewSet (Only READ support)
class ArticleReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


# user viewset
class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class UserModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Full Example: UserViewSet with multiple @action patterns
class UserActionViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Custom POST action with overridden permission and custom serializer
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET action on the full collection
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def recent_users(self, request):
        recent_users = User.objects.order_by('-last_login')[:5]
        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)

    # Extra action supporting PUT (update password) and DELETE (unset)
    @action(detail=True, methods=["put"], name="Change Password")
    def password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @password.mapping.delete
    def delete_password(self, request, pk=None):
        user = self.get_object()
        user.set_password("")  # Not recommended in real-world apps
        user.save()
        return Response({'status': 'password deleted'})

    # Example usage of reverse_action
    @action(detail=False, methods=["get"])
    def action_links(self, request):
        return Response({
            'set_password_url': self.reverse_action('set-password', args=['1']),
            'recent_users_url': self.reverse_action(self.recent_users.url_name),
            'password_put_url': self.reverse_action('password', args=['1']),
        })



# caching 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core.cache import cache


@cache_page(60*10)
@vary_on_cookie
@api_view(["GET"])
def get_user_name(request):
    content = {'user_feed': request.user.username}
    return Response(content)
    

class BlogCacheView(APIView):
    @method_decorator(cache_page(60 * 60))  # 1 hour
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request):
        # data = {"title": Blog.objects.get(id=1).title}
        
        blog = get_object_or_404(Blog, id=1)
        data = {"title": blog.title}

        # try:
        #     blog = Blog.objects.get(id=1)
        #     data = {"title": blog.title}
        # except Blog.DoesNotExist:
        #     data = {"title": "Not found"}

        return Response(data)


class ProfileViewCache(viewsets.ViewSet):
    # With auth: cache requested url for each user for 2 hours
    # @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(cache_page(60))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, format=None):
        content = {
            "user_name": request.user.username
        }
        return Response(content)
    

class UserFeedView(APIView):
    def get(self, request):
        user_id = request.user.id
        name = request.user.username
        cache_key = f"user_feed_{user_id}"
        data = cache.get(cache_key)
        # blog = get_object_or_404(Blog, id=1).title
        blog =  Blog.objects.get(id=1).title
        if not data:
            # Simulate expensive logic
            data = {"name": name,
                    "blog": blog,
                    "feed": f"Expensive data for user {user_id}"
                    }
            cache.set(cache_key, data, timeout=60)  # 60seconds

        return Response(data)



# throttle 

from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, SimpleRateThrottle
    
@api_view(['GET'])
# @throttle_classes([UserRateThrottle])
def example_throttle_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)


class ExampleThrottleView(APIView):
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
    

class MyViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"], throttle_classes=[UserRateThrottle])
    def limited(self, request):
        return Response({"message": "Throttled endpoint"})


# custom throttle
class CustomThrottle(UserRateThrottle):
    scope = 'custom_scope'

    def get_rate(self):
        return '5/min'
    
@api_view(['GET'])
@throttle_classes([CustomThrottle])
def custom_example_throttle_view(request, format=None):
    return Response({'status': 'This view allows 5 requests per minute'})

# class CustomThrottle(SimpleRateThrottle):
#     def get_cache_key(self, request, view):
#         if request.user.is_authenticated:
#             # Use user ID to throttle
#             return self.cache_format % {
#                 'scope': 'custom_user',
#                 'ident': request.user.pk
#             }
#         else:
#             # Use IP for anonymous users
#             ident = self.get_ident(request)
#             return self.cache_format % {
#                 'scope': 'custom_anon',
#                 'ident': ident
#             }

#     def get_rate(self):
#         # Override to use separate logic per user type
#         if self.scope == 'custom_user':
#             return '6/day'
#         elif self.scope == 'custom_anon':
#             return '3/day'

class CustomUserThrottle(UserRateThrottle):
    scope = 'custom_user'


class CustomAnonThrottle(AnonRateThrottle):
    scope = 'custom_anon'


@api_view(['GET'])
@throttle_classes([CustomUserThrottle, CustomAnonThrottle])
def custom_view(request):
    return Response({"message": "Hello, throttled world!"})

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'


class MyThrottledView(APIView):
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    def get(self, request, format=None):
        return Response({'message': 'This is throttled by burst and sustained rates.'})
