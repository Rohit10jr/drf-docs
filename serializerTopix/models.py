from django.db import models
from django.contrib.auth.models import User

class TempUser(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username}"


class Comments(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(TempUser, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True)
    int_a = models.IntegerField(null=True)
    int_b = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.email} - {self.content[:20]}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()


class Reaction(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='comment')
    content = models.TextField()


class Account(models.Model):
    account_name = models.CharField()
    user_type = models.CharField()
    created = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published = models.DateField()


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.CharField(null=True)


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Novel(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class DataPointColor(models.Model):
    name = models.CharField(max_length=100)
    color = models.JSONField(null=True)
    label = models.CharField(max_length=50)
    x_coordinate = models.SmallIntegerField(null=True)
    y_coordinate = models.SmallIntegerField(null=True)

    def __str__(self):
        return f"{self.name} {self.label}"



class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
    


# validators
class TechArticle(models.Model):
    title = models.CharField(max_length=100, unique=True)  # Will still use UniqueValidator in serializer
    slug = models.SlugField(max_length=100)
    category = models.CharField(max_length=50)
    position = models.PositiveIntegerField()
    published = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category', 'position')  # DB-level; we'll enforce at serializer too

    def __str__(self):
        return self.title
    

class BillingRecord(models.Model):
    client = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)


# signal for creating token automatically
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)