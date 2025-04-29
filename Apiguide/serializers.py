from rest_framework import serializers
from .models import Book
from rest_framework.reverse import reverse
from django.urls import reverse_lazy


class BookSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('book-detail', kwargs={"pk":obj.pk}, request=request)
        # return reverse_lazy('book-detail', kwargs={"pk":obj.pk})