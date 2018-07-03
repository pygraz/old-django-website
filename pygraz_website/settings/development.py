from .base import *
from captcha import constants as captcha_constants

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SOUTH_TESTS_MIGRATE = False
SECRET_KEY = 'SECRET_KEY'
RECAPTCHA_PUBLIC_KEY = captcha_constants.TEST_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = captcha_constants.TEST_PRIVATE_KEY
POSTMARK_TEST_MODE = True
POSTMARK_API_KEY = "test-token"
