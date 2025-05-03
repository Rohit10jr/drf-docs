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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.core.serializers import serialize
import json
from .serializers import UserSerializer
from rest_framework.decorators import api_view, schema, renderer_classes
from rest_framework.schemas import AutoSchema

from rest_framework.renderers import JSONOpenAPIRenderer, JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer

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
    

# requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class RequestInspectorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            stream_data = request.stream.read().decode('utf-8')
            #  request.stream is a file-like object, but it's not guaranteed to have a .closed attribute like a regular file does. So, trying to access .closed directly on request.stream raises that AttributeError.
        except Exception as e:
            stream_data = f"Could not read stream: {str(e)}"

        return Response({
            "data": request.data,
            "query_params": request.query_params,
            "parsers": [parser.__class__.__name__ for parser in request.parsers],
            "user": str(request.user),
            "auth": str(request.auth),
            "authenticators": [auth.__class__.__name__ for auth in request.authenticators],
            "method": request.method,
            "content_type": request.content_type,
            "stream": stream_data
        })
    
    # def get(self, request, *args, **kwargs):
    #     # Data to be serialized in the Response
    #     data = {
    #         "message": "This is a demonstration of the DRF Response object",
    #         "user": str(request.user)
    #     }

    #     # Create Response object
    #     response = Response(data, status=202, template_name='dummy.html')

    #     # Access attributes BEFORE rendering
    #     response_info = {
    #         "data": response.data,
    #         "status_code": response.status_code,
    #         "template_name": response.template_name,
    #         "accepted_renderer": str(response.accepted_renderer),
    #         "accepted_media_type": response.accepted_media_type,
    #         "renderer_context": response.renderer_context,
    #         # Don't access .content before rendering, or it might raise an error
    #     }

    #     # Call .render() manually (optional, usually done by DRF automatically)
    #     response.render()

    #     # Add rendered content to the response info
    #     response_info["content"] = response.content.decode('utf-8')

    #     # Return everything as a fresh response
    #     return Response(response_info)
    

    def get(self, request, *args, **kwargs):
        # Data to be serialized in the Response
        data = {
            "message": "This is a demonstration of the DRF Response object",
            "user": str(request.user)
        }

        # Just return it — DRF will inject content negotiation fields
        return Response(data, status=202, template_name='dummy.html')
    


#  views 

@api_view()
def hello_world(request):
    return Response({"messages": "hello world"})


@api_view(['GET', 'POST'])
def hello_world_2(request):
    if request.method == 'POST':
        # return Response({"message": "Got some data!", "data": request.data})
        # return Response({
        #     "message": "Hello!",
        #     "user": {
        #         "id": request.user.id,
        #         "username": request.user.username,
        #         "email": request.user.email
        #     }
        # })

        # Option 2: Use Django's built-in serializer
        # user_json = json.loads(serialize('json', [request.user]))[0]['fields']
        # return Response({"user": user_json})
    
        # Option 3: Use a DRF serializer
        user_data = UserSerializer(request.user).data
        return Response({"user": user_data})

    return Response({"message": "Hello, world!"})


class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'

@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
def hello_world_3(request):
    return Response({"message": "Hello for today! See you tomorrow!"})


class OneMinuteThrottle(UserRateThrottle):
    # rate = '1/min'
    rate = '6/min'
    # rate = '20/second' 

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes, authentication_classes, permission_classes


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([OneMinuteThrottle])
def greet_user(request):
    return Response({"message": f"Hi {request.user.username}, you can only see this once a minute!"})


class EchoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        return Response({"you_sent": data})
    
class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)



@api_view(['GET'])
@schema(None)
def schema_view(request):
    return Response({"message": "Will not appear in schema!"})



from rest_framework.schemas.openapi import AutoSchema
from rest_framework.schemas.utils import is_list_view
from rest_framework import serializers
from rest_framework.compat import coreapi, coreschema

class CustomAutoSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() == 'get':
            extra_fields = [
                coreapi.Field(
                    name="sample_param",
                    required=False,
                    location="query",
                    schema=coreschema.String(
                        description="A sample query parameter"
                    )
                )
            ]
        return super().get_manual_fields(path, method) + extra_fields
    

class SimpleSchema(AutoSchema):
    def get_description(self, path, method):
        return "This is a simple custom description for this endpoint."



@api_view(['GET'])
@schema(CustomAutoSchema())
# @schema(SimpleSchema())
def schema_view_2(request):
    return Response({"message": "Hello for today! See you tomorrow!"})
    



# renderers


class UserCountView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user_count = User.objects.filter(is_active=True).count()
        content = {'user_count': user_count}
        return Response(content)
    
    
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def user_count_view(request, format=None):
    """
    A view that returns the count of active users in JSON.
    """
    user_count = User.objects.filter(is_active=True).count()
    content = {'user_count': user_count}
    return Response(content)

# 1️⃣ JSONRenderer
class ProductJSONView(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        # product = self.get_object()
        product = self.get_queryset()
        serializer = self.get_serializer(product,  many=True)
        return Response(serializer.data)
    
# 2️⃣ TemplateHTMLRenderer
class ProductDetailHTMLView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        return Response({'product': product}, template_name='product.html')
    

# 3️⃣ StaticHTMLRenderer
@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def static_html_view(request):
    data = """
    <html>
        <head><title>Welcome</title></head>
        <body>
            <h1>Hello, this is static HTML!</h1>
            <p>This is a pre-rendered response.</p>
        </body>
    </html>
    """
    return Response(data)