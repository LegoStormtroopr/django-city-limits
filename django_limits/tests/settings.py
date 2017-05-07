from django.apps import apps

INSTALLED_APPS = ('django_limits','django_limits.tests')

SECRET_KEY = 'tina_turner_and_hugh_laurie'
MODEL_LIMIT_CLASS = 'django_limits.tests.limiter.NutbushLimiter'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    # 'NAME': ':memory:',
    'NAME': 'test.db'
  }
}
