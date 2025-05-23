from rest_framework import serializers
from .models import Book, Product
from rest_framework.reverse import reverse
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'url', 'description']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('book-detail', kwargs={"pk":obj.pk}, request=request)
        # return reverse_lazy('book-detail', kwargs={"pk":obj.pk})

    def validate_title(self, value):
        print("3. inside serializer")
        if "badword" in value.lower():
            raise serializers.ValidationError("Inappropriate word in title.")
        return value
    
    def validate(self, data):
        print("4. inside serializer")
        if len(data.get('description', '')) < 3:
            raise serializers.ValidationError({
            'description': "Description must be at least 3 characters long."
        })
        return data
    


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # # This ensures it can handle both single and multiple objects
    # def to_internal_value(self, data):
    #     if isinstance(data, list):
    #         return [super().to_internal_value(item) for item in data]
    #     return super().to_internal_value(data)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProductUrlSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'price', 'url']