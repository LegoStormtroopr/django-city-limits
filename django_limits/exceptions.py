from django.core import exceptions


class LimitExceeded(exceptions.PermissionDenied):
    def __init__(self, model, details, template=None, *args, **kwargs):
        self.details = details
        self.model = model
        self.template = template
        super(LimitExceeded, self).__init__(*args, **kwargs)

    def __str__(self):
        return "LimitExceeded - Your plan only allows for {number} {name} - {message}".format(
            number=self.details['limit'],
            message=self.details['message'],
            name=self.model._meta.verbose_name_plural
        )
