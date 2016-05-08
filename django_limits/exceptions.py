from django.core import exceptions


class LimitExceeded(exceptions.PermissionDenied):
    def __init__(self, model, details, *args, **kwargs):
        self.details = details
        self.model = model
        super(LimitExceeded, self).__init__(*args, **kwargs)
    def __str__(self):
        return "LimitExceeded - Your plan only allows for %s %s"%(self.details['max'],self.model._meta.verbose_name_plural)
