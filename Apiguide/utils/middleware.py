# middleware.py
class ResponseDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if it's a DRF Response and has these attributes
        if hasattr(response, 'accepted_renderer'):
            print("== DRF Response Debug ==")
            print("Renderer:", response.accepted_renderer)
            print("Media Type:", response.accepted_media_type)
            print("Context:", response.renderer_context)

        return response
