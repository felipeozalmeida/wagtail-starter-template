from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DJANGO_DEBUG', False))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DATABASE_HOST'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'PORT': os.environ.get('DATABASE_PORT'),
        'USER': os.environ.get('DATABASE_USER'),
    }
}


# Static files

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_DEFAULT_ACL = os.environ.get('AWS_DEFAULT_ACL')
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False


# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT'))
EMAIL_USE_TLS = bool(os.environ.get('EMAIL_USE_TLS'))
