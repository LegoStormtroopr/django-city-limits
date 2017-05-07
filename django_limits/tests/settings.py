import os
from django.apps import apps

INSTALLED_APPS = ('django_limits', 'django_limits.tests')

MIDDLEWARE_CLASSES = ['django_limits.middleware.LimitExceededMiddleware']

SECRET_KEY = 'sorry_tina_turner_and_hugh_laurie'
MODEL_LIMIT_CLASS = 'django_limits.tests.limiter.NutbushLimiter'

if os.environ.get('DB') == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'aristotle_test_db',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
elif os.environ.get('DB') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test.db'
        }
    }
