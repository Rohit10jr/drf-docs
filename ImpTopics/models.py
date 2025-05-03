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

# solution for n + 1 problem

# ⚠️ Short Answer: What is the N+1 Problem?
# The N+1 problem happens when:
# You run 1 query to fetch N parent objects (e.g., Order)
# Then run N additional queries to fetch related data (e.g., Customer for each Order)
# This leads to performance issues.

# def get_queryset(self):
    # return Order.objects.select_related('customer').prefetch_related('items')


class Purchase(models.Model):
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} by {self.purchaser.username}"
    



class Product(models.Model):
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('books', 'Books'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name