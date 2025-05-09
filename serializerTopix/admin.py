from django.contrib import admin
from .models import Comments, TempUser, Account, Category, News, Book, UserProfile, Author, Novel, DataPointColor, Track, Album, BillingRecord,TechArticle

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
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(BillingRecord)
admin.site.register(TechArticle)


from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']