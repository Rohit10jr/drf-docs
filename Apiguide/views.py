from django.shortcuts import render
from .models import Book 
from .serializers import BookSerializer
from rest_framework import generics
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm 
from rest_framework.reverse import reverse
from django.http import HttpResponse, Http404
from django.views import View
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import APIException
# Create your views here.


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable.'
    default_code = 'service_unavailable'


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateViewApi(CreateAPIView):
    print("1. inside view")
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Handles the full POST request logic in views like CreateAPIView.
    def create(self, request, *args, **kwargs):
        raise ServiceUnavailable()
        # if external_service_is_down():
        #     raise ServiceUnavailable()
        # return super().create(request, *args, **kwargs)

    # example of create method
    # def create(self, request, *args, **kwargs):
    #     # Create the serializer instance, passing the incoming request data
    #     serializer = self.get_serializer(data=request.data)
        
    #     # Perform field and object-level validation and populates serializer.validated_data. If validation fails, a ValidationError is raised
    #     serializer.is_valid(raise_exception=True)
        
    #     # Save the validated data, creating the object in the database
    #     self.perform_create(serializer)
        
    #     # Return a 201 response with the serialized data of the created object
    #     return Response(serializer.data, status=201)

    
    # Called after serializer is validated. You override this to customize how the object is saved (e.g., add request.user, simulate errors).
    # def perform_create(self, serializer):
        # raise Exception("Simulated server crash")


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
    

