from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SOUTH_TESTS_MIGRATE = False
SECRET_KEY = 'SECRET_KEY'
RECAPTCHA_PUBLIC_KEY = 'RECAPTCHA_PUBLIC_KEY'
RECAPTCHA_PRIVATE_KEY = 'RECAPTCHA_PRIVATE_KEY'
