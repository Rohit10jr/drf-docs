from django.shortcuts import render
from .models import Book 
from .serializers import BookSerializer
from rest_framework import generics
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm 
from rest_framework.reverse import reverse
# Create your views here.


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'Apiguide/book_form.html'
    success_url = reverse_lazy('book-list')

    
    def form_valid(self, form):
        # You can use the serializer for additional validation if necessary
        # But it's better to use form_cleaned_data to do so
        # serializer = BookSerializer(data=form.cleaned_data)
        # if serializer.is_valid():
        #     serializer.save()
        return super().form_valid(form)