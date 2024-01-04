"""
Django settings for ejar project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y3rp$t@ya6$mfq1z30)x=l+-@h87y%2zkv5lg$u%+@^69#wmi6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'units.apps.UnitsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myejar.apps.MyejarConfig',
    'mathfilters',
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


TWILIO_ACCOUNT_SID = 'AC06e1943db32a3b12262ae75a1bf63fe6'
TWILIO_AUTH_TOKEN = 'b7bc7719067659fb78a05f2c68a7b9ff'
TWILIO_PHONE_NUMBER = '+15855777097'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'ejar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ejar.wsgi.application'

import dj_database_url

DATABASE_URL = "postgresql://postgres:agCGCa4B6dF223A66aA445A2GG-dCb2f@viaduct.proxy.rlwy.net:55333/railway"
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#DATABASES = {
#   'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  'ejar',
        'USER':  'postgres',
        'PASSWORD':  'Break567@',
        'HOST':  'localhost',
        'PORT':  '5432',

    }
}

DATABASES ={
    "default" : dj_database_url.config(default=DATABASE_URL, conn_max_age=1000)
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'ejar/static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


CSRF_TRUSTED_ORIGINS = ['https://www.waqf1.com']


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'