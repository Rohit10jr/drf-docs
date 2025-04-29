from django.contrib import admin
from .models import Book

# option 1 = Decorator - not working
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'published_date')
#     search_fields = ('title', 'author')
#     list_filter = ('published_date',)

# option 2 = classic - working with search filter display options
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author')
    list_filter = ('title',)

admin.site.register(Book, BookAdmin)

# option3 = quick default
# admin.site.register(Book)