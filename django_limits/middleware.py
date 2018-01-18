from django_limits.exceptions import LimitExceeded
from django_limits.views import limit_exceeded_view


class LimitExceededMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, LimitExceeded):
            return limit_exceeded_view(
                request,
                limit_exception=exception,
                template=exception.template
            )
        return None
