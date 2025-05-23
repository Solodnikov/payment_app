from threading import local

_thread_data = local()


class CurrentRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_data.request = request
        response = self.get_response(request)
        return response
