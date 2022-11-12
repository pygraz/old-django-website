from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pygraz-django',
        'USER': 'postgres',
        'PASSWORD': 'deMo.123',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

SOUTH_TESTS_MIGRATE = False
SECRET_KEY = "SECRET_KEY"
POSTMARK_TEST_MODE = True
POSTMARK_API_KEY = "test-token"
