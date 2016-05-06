from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete
from django.dispatch import receiver

from django_limits import exceptions


MODEL_LIMITS = getattr(settings, 'MODEL_LIMITS')


@receiver(pre_save)
def check_limits(sender, **kwargs):
    if sender in MODEL_LIMITS.keys():
        queryset = MODEL_LIMITS[sender].get('queryset', sender.objects)
        if queryset.count() > MODEL_LIMITS[sender]['max']:
            raise exceptions.LimitExceeded(model=sender,details=MODEL_LIMITS[sender])
