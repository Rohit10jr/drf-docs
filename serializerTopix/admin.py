from django.contrib import admin
from .models import Comments, TempUser, Account, Category, News, Book, UserProfile, Author, Novel, DataPointColor, Track, Album, BillingRecord,TechArticle, Docs
from .models import Comments, TempUser, Account, Category, News, Book, UserProfile, Author, Novel, DataPointColor, Track, Album, BillingRecord,TechArticle, Docs
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

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
admin.site.register(Docs)

# class CustomUserAdmin(UserAdmin):
#     list_display = ['id', 'username', 'email', 'is_staff', 'is_superuser']
#     list_display = ['id'] + list(DefaultUserAdmin.list_display)


class CustomUserAdmin(DefaultUserAdmin):
    # Add 'id' to the list display
    list_display = ['id'] + list(DefaultUserAdmin.list_display)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# from rest_framework.authtoken.admin import TokenAdmin

# TokenAdmin.raw_id_fields = ['user']