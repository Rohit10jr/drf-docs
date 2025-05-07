from django.shortcuts import render
from rest_framework import generics
from .models import Comments, Post, Account, News, Category, Book, UserProfile, Novel, DataPointColor, Album, Track
from .serializers import CommentSerializer, NewsSerializer, CommentModelSerializer, UserProfileSerializer, NovelSerializer, DataPointColorSerializer, PostSerializer, AccountSerializer, BookSerializer, AlbumSerializer, TrackSerializer, TrackHyperLinkSerializer, AlbumHyperLinkSerializer
from datetime import datetime
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.

# class Comment:
#     def __init__(self, email, content, created=None):
#         self.email = email
#         self.content = content
#         self.created = created or datetime.now()

# comment = Comment(email='leila@example.com', content='foo bar')

# class CommentSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     content = serializers.CharField(max_length=200)
#     created = serializers.DateTimeField()

# serializer = CommentSerializer(comment)
# print(serializer.data)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer


# Custom save options to send mail
# def send_email(email, message):
#     pass

# class ContactForm(serializers.Serializer):
#     email = serializers.EmailField()
#     message = serializers.CharField()

#     def save(self):
#         email = self.validated_data['email']
#         message = self.validated_data['message']
#         send_email(from=email, message=message)



@api_view(['GET', 'POST'])
def comment_list_create(request):
    if request.method == 'GET':
        comments = Comments.objects.all()
        # serializer = CommentSerializer(comments, many=True)
        serializer = CommentModelSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # serializer = CommentSerializer(data=request.data)
        serializer = CommentModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, pk):
    try:
        comment = Comments.objects.get(pk=pk)
    except Comments.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # serializer = CommentSerializer(comment)
        serializer = CommentModelSerializer(comment)
        print(serializer.instance) 
        # print(serializer.initial_data)  
        return Response(serializer.data)

    elif request.method == 'PUT':
        # serializer = CommentSerializer(comment, data=request.data)
        serializer = CommentModelSerializer(comment, data=request.data,partial=True)
        if serializer.is_valid():
            print(serializer.instance)  # The same Comments object with pk=1
            print(serializer.initial_data) # {'email': 'test@example.com', 'content': 'Updated comment'}
        # if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# CREATE + LIST
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# RETRIEVE + UPDATE + DELETE
class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


# news genercis
# class NewsListCreateView(ListCreateAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}  # needed for absolute URLs

# class NewsDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#     lookup_field = 'pk'

#     def get_serializer_context(self):
#         return {'request': self.request}



class NewsListCreateView(APIView):
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(News, pk=pk)

    def get(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsSerializer(news, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsSerializer(news, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        news = self.get_object(pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookBulkUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_object(self):
        # Override to return the full queryset for bulk update
        return self.get_queryset()
    

# class BookListCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = BookSerializer(data=request.data, many=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# # For bulk update
# class BookBulkUpdateView(APIView):
#     def put(self, request, *args, **kwargs):
#         # You must pass all the current objects (like with a filter)
#         ids = [item['id'] for item in request.data if 'id' in item]
#         books = Book.objects.filter(id__in=ids)
#         serializer = BookSerializer(books, data=request.data, many=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class BookBulkCreateView(generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     def get_serializer(self, *args, **kwargs):
#         kwargs['many'] = True  # 👈 force many=True
#         return super().get_serializer(*args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class BookBulkUpdateView(generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     def get_serializer(self, *args, **kwargs):
#         kwargs['many'] = True  # 👈 force many=True for bulk update
#         return super().get_serializer(*args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         # Extract the IDs from the request data to match books
#         ids = [item['id'] for item in request.data if 'id' in item]
#         books = Book.objects.filter(id__in=ids)

#         # Validate and update the books
#         serializer = self.get_serializer(books, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_200_OK)



class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileApiview(APIView):
    def get(self, request):
        userprofile = UserProfile.objects.all()
        # Get fields from query params: ?fields=username,email
        fields_param = request.query_params.get('fields')
        if fields_param:
            fields = [f.strip() for f in fields_param.split(',')]
        else:
            fields = None

        serializer = UserProfileSerializer(userprofile, many=True, fields=fields)
        return Response(serializer.data)
    
    def post(self, request):
        many = isinstance(request.data, list)
         # 👇 Get fields from query params (optional)
        fields_param = request.query_params.get('fields')
        if fields_param:
            fields = [f.strip() for f in fields_param.split(',')]
        else:
            fields = None

        serializer = UserProfileSerializer(data=request.data, many=many, fields=fields)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(UserProfile, pk=pk)

    def get(self, request, pk):
        user_profile = self.get_object(pk)
        # 👇 Support dynamic fields via query param: ?fields=username,bio
        fields_param = request.query_params.get('fields')
        if fields_param:
            fields = [f.strip() for f in fields_param.split(',')]
        else:
            fields = None

        serializer = UserProfileSerializer(user_profile, fields=fields)
        return Response(serializer.data)

    def put(self, request, pk):
        user_profile = self.get_object(pk)
        # 👇 Allow dynamic fields (optional)
        fields_param = request.query_params.get('fields')
        if fields_param:
            fields = [f.strip() for f in fields_param.split(',')]
        else:
            fields = None

        serializer = UserProfileSerializer(user_profile, data=request.data, fields=fields, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    """I dont think its a good implementation
    NotImplementedError: Serializers with many=True do not support multiple update by default, only multiple create. For updates it is unclear how to deal with insertions and deletions. If you need to support multiple update, use a `ListSerializer` class and override `.update()` so you can specify the behavior exactly."""
    # put method to allow both single and bulk partial updates dynamically:
    # def put(self, request, pk):
    #     many = isinstance(request.data, list)

    #     if many:
    #         # Bulk partial update — ensure each item has an 'id'
    #         ids = [item.get('id') for item in request.data]
    #         if not all(ids):
    #             return Response({"error": "Each object must include an 'id' field for bulk update."},
    #                             status=status.HTTP_400_BAD_REQUEST)

    #         instances = UserProfile.objects.filter(id__in=ids)
    #         instance_map = {obj.id: obj for obj in instances}
    #         updated_instances = [instance_map.get(item['id']) for item in request.data]

    #         serializer = UserProfileSerializer(updated_instances, data=request.data, many=True, partial=True)
    #     else:
            # Single partial update
            # pk = request.data.get('id')
            # if not pk:
            #     return Response({"error": "ID is required for single update."},
                                # status=status.HTTP_400_BAD_REQUEST)
            # instance = get_object_or_404(UserProfile, id=pk)

        #     user_profile = self.get_object(pk)
        #     serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_profile = self.get_object(pk)
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# cutom API endpoint with PATCH method to handle bulk update in apiview
# class BulkUserProfileUpdate(APIView):
#     def patch(self, request):
#         is_many = isinstance(request.data, list)
#         serializer = UserProfileSerializer(data=request.data, many=is_many, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

class NovelListCreateView(generics.ListCreateAPIView):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer

class NovelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    # lookup_field = 'pk'


class DataPointColorListCreateView(generics.ListCreateAPIView):
    queryset = DataPointColor.objects.all()
    serializer_class = DataPointColorSerializer


class DataPointColorDetailView(generics.RetrieveUpdateAPIView):
    queryset = DataPointColor.objects.all()
    serializer_class = DataPointColorSerializer

# serializer fields
class AlbumListCreateView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class TrackListCreateView(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumHyperLinkSerializer

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackHyperLinkSerializer


