from django_limits.exceptions import LimitExceeded
from django_limits.views import limit_exceeded_view


class LimitExceededMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, LimitExceeded):
            return limit_exceeded_view(
                request,
                limit_exception=exception,
                template=exception.template
            )
        return None
