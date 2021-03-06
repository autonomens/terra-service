"""
Django settings

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import copy
import os
from datetime import timedelta

from django.utils.log import DEFAULT_LOGGING

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(PROJECT_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)
PROJECT_NAME = os.path.basename(PROJECT_DIR)
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'geoinsee',
    'geocoding',
    'geoip',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locales'),
)
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

FORMAT_MODULE_PATH = [
    PROJECT_NAME + '.formats',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')

# Just to be easily override by children conf files.
LOGGING = copy.deepcopy(DEFAULT_LOGGING)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'permissions.IsJWTAuthenticated',
    )
}

INSEE_API_URL = 'http://rdf.insee.fr/sparql'

GEOCODING_PROVIDER = 'geocoding.backend.providers.OpenCage'

# Code SRID for projection in database
# Check https://epsg.io/3857
SRID = 3857

