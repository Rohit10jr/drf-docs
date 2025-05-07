from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

# PageNumberPagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow client to override it using ?page_size=
    max_page_size = 15  # Limit max value of ?page_size=
    page_query_param = 'page'  # Default is 'page'
    last_page_strings = ['last']  # Allow ?page=last



class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
    
# LimitOffSetPagination
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'


# CursorPagination.py
class ProductCursorPagination(CursorPagination):
    page_size = 5
    cursor_query_param = 'cursor'
    ordering = 'created_at'  # newest first

