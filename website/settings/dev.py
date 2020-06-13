from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&rvqqj+j3v*gci0&#*322n^$yrw8n4b_xcv8^g%udk)hwvb%2#'


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

