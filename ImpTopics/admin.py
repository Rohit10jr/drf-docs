from django.contrib import admin
from .models import Post, Order, Blog, Purchase,Product
# Register your models here.

admin.site.register(Post),
admin.site.register(Order),
admin.site.register(Blog),
admin.site.register(Purchase),
admin.site.register(Product),