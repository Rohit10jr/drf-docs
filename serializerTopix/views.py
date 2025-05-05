from django.shortcuts import render
from rest_framework import generics
from .models import Comments, Post
from .serializers import CommentSerializer, CommentModelSerializer, PostSerializer
from datetime import datetime
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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