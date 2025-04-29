from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print("inside custom exception")
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['error'] = True
        response.data['message'] = response.data.get('detail', 'Something went wrong')

    return response
