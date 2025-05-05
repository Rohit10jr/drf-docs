from django.db import models


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