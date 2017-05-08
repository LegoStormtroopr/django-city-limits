from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.module_loading import import_string

from django_limits import exceptions


@receiver(pre_save)
def check_limits(sender, **kwargs):
    limiter = import_string(settings.MODEL_LIMIT_CLASS)()
    limiter(model=sender, **kwargs)
