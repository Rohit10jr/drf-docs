# myapp/negotiation.py
from rest_framework.negotiation import BaseContentNegotiation

class IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        # Always pick the first parser, ignore Content-Type header
        return parsers[0]
    
    # def select_parser(self, request, parsers):
    #     return super().select_parser(request, parsers)
    
    def select_renderer(self, request, renderers, format_suffix):
        # Always pick the first renderer, ignore Accept header
        return (renderers[0], renderers[0].media_type)
