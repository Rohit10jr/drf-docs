from django.contrib import admin
from .models import Comments, TempUser
# Register your models here.

admin.site.register(Comments)
admin.site.register(TempUser)