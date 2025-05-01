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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.metadata import SimpleMetadata
from rest_framework import viewsets
from rest_framework.decorators import action
from Apiguide.utils.negotiation import IgnoreClientContentNegotiation

from Apiguide.utils.pagination import StandardResultsSetPagination, CustomLimitOffsetPagination, ProductCursorPagination,CustomPagination
from .models import Product
from .serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from drf_spectacular.utils import extend_schema
# Create your views here.


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable.'
    default_code = 'service_unavailable'


class BookList(generics.ListAPIView):

    # metadata_class = SimpleMetadata
    """
    Returns a list of books or creates a new one.
    """

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
    



# Meta data apiguide
class MyCustomView(APIView):
    metadata_class = SimpleMetadata

    def get(self, request, format=None):
        return Response({"message": "Hello world"})
    

class GlobalMetadataView(APIView):
    def get(self, request, format=None):
        return Response({"message": "Global metadata is used."})
    

class PerViewMetadataView(APIView):
    metadata_class = SimpleMetadata

    def get(self, request, format=None):
        # """get for metadata."""
        return Response({"message": "This view uses per-view metadata."})
    

class SchemaViewSet(viewsets.ViewSet):
    metadata_class = SimpleMetadata

    @action(methods=['get'], detail=False)
    def api_schema(self, request):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        return Response(data)
    

class MinimalExampleView(APIView):

    def get_view_description(self, html=False):
        return "Custom description for this Minimal endpoint"
    
    def get(self, request, format=None):
        """get for metadata."""
        
        return Response({"message": "Using minimal metadata!"})


# content negotiation
class NoNegotiationView(APIView):
    """
    An example view that does not perform content negotiation.
    """
    content_negotiation_class = IgnoreClientContentNegotiation

    def get(self, request, format=None):
        return Response({
            'accepted media type': request.accepted_renderer.media_type
        })


# format suffixes
class CommentList(APIView):
    def get(self, request, format=None):
        return Response({"message": "List of comments"})

    def post(self, request, format=None):
        return Response({"message": "Comment created"})
    

# pagination

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    # queryset = Product.objects.all().order_by('created_at')
    serializer_class = ProductSerializer
    # pagination_class = StandardResultsSetPagination
    # pagination_class = CustomLimitOffsetPagination
    # pagination_class = ProductCursorPagination
    pagination_class = CustomPagination


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('created_at')
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(self.request.data, list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
    


# schema 

# class CustomSchema(AutoSchema):
#     def get_operation(self, path, method):
#         operation = super().get_operation(path, method)
#         operation["summary"] = "Custom summary for this endpoint"
#         return operation


# class CustomSchema(AutoSchema):
#     def get_tags(self, path, method):
#         return ["CustomTag"]

#     def get_operation_id(self, path, method):
#         return f"custom_{method.lower()}_op"

#     def map_field(self, field):
#         if hasattr(field, 'custom_info'):
#             return {"type": "string", "description": "Custom field"}
#         return super().map_field(field)


@extend_schema(tags=["Hello"])
class HelloView(APIView):
    # schema = CustomSchema()
    # schema = CustomSchema(component_name="MyComponent")

    @extend_schema(
        # request=UserSerializer,
        # responses=UserSerializer,
        tags=["User Signup"],
        description="greet a hello world"
    )
    def get(self, request):
        return Response({"message": "Hello World"})
    

from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning

# versioning

class ExampleQueryVersioning(QueryParameterVersioning):
# class ExampleQueryVersioning(URLPathVersioning):
    default_version = 'v1'
    allowed_versions = ['1.0', '2.0']
    version_param = 'v'


class QueryVersionAPI(APIView):
    # versioning_class = QueryParameterVersioning
    versioning_class = ExampleQueryVersioning

    def get(self, request):
        return Response({'version': request.version, "message": "this is query versioning"})

class DefaultVersionAPI(APIView):

    def get(self, request, *args, **kwargs):
        return Response({
            'version': request.version,
            'message': 'Hello from DefaultVersionAPI'
        })