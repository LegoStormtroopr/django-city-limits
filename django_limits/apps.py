from django.apps import AppConfig


class DjangoLimiterAppConfig(AppConfig):
    name = 'django_limits'

    def ready(self):
        import django_limits.signals
