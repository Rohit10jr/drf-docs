from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
    

class Order(models.Model):
    customer_id = models.IntegerField()
    order_number = models.CharField(max_length=20)
    description = models.TextField()
