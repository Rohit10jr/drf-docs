from django.contrib import admin
from .models import Post, Order, Blog
# Register your models here.

admin.site.register(Post),
admin.site.register(Order),
admin.site.register(Blog),