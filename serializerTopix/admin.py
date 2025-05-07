from django.contrib import admin
from .models import Comments, TempUser, Account, Category, News, Book, UserProfile, Author, Novel, DataPointColor
# Register your models here.

admin.site.register(Comments)
admin.site.register(TempUser)
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(News)
admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(Novel)
admin.site.register(Author)
admin.site.register(DataPointColor)