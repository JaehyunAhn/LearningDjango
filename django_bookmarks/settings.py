# -*- coding: utf-8 -*-
"""
Django settings for django_bookmarks project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import os.path

SITE_HOST = '127.0.0.1:8000'
DEFAULT_FROM_EMAIL = '장고 북마크 <django.bookmarks@example.com>'
EMAIL_HOST = 'mail.yourisp.com'
EMAIL_PORT = ''
EMAIL_HOST_USER = 'username+mail.yourisp.com'
EMAIL_HOST_PASSWORD = ''
SITE_ID = 1

# Cashing
CACHE_BACKEND = 'simple:///'
CACHE_MIDDLEWARE_SECONDS = 60 * 5 # 5 mins to Caching

# for Translation
USE_I18N =True
LANGUAGE_CODE = 'kr'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (
		os.path.join(os.path.dirname(__file__), 'templates'),
		)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%v+!dy#)z#)h@2yq0a&9*np6jpaosf_!pq1qzn=p-6y3n0haz1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# allow 'pytz' data config
USE_TZ = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django.contrib.comments',
	'django.contrib.sites',
	'django_bookmarks.bookmarks',
    'django_bookmarks.todolist',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ADMINS = (
    # Post code errors to my email
    ('sogosonnet', 'sogosonnet@gmail.com'),
)

ROOT_URLCONF = 'django_bookmarks.urls'

WSGI_APPLICATION = 'django_bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
