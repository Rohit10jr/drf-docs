from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog, Post, Article, Order, Purchase, Product
from rest_framework.serializers import Serializer, CharField

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']  # Less detail

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class PasswordSerializer(Serializer):
    password = CharField(write_only=True, required=True)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'product_name', 'price', 'purchased_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'in_stock']