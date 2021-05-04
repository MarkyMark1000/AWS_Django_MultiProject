"""
Django settings for brokerdata project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

# standard imports
from pathlib import Path
import os
# import mysql.connector
# imports from extra_code_or_config
from brokerdata.extra_code_or_config.getIP import appendIPToArray
from brokerdata.extra_code_or_config.hidden_account import LIVE_DB_NAME, \
            LIVE_DB_USER, LIVE_DB_PASSWORD, LIVE_DB_HOST, LIVE_DB_PORT, \
            TEST_DB_NAME, TEST_DB_USER, TEST_DB_PASSWORD, TEST_DB_HOST, \
            TEST_DB_PORT, DOCK_DB_NAME, DOCK_DB_USER, DOCK_DB_PASSWORD, \
            DOCK_DB_HOST, DOCK_DB_PORT

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!1zgm*)*6r&zp7ix&hm*^#h50%g!&$@r^-!^e)*0=6=ram9dq8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DJANGO_DEBUG', False))


ALLOWED_HOSTS = ["localhost",
                 "127.0.0.1",
                 "brokerdata.6hbnjaadkuqb2.eu-west-2.cs.amazonlightsail.com", # lightsail
                 "contparallax-env.eba-fkmkqc92.eu-west-2.elasticbeanstalk.com"] # elastic beanstalk

# Append EC2 ip to ALLOWED_HOSTS to prevent unnecessary logs
# or health degredation.
appendIPToArray(ALLOWED_HOSTS)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.backend',
    'apps.frontend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',       # mjw - whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'brokerdata.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'brokerdata.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Can determine if using test or production database
API_ENVIRONMENT = str(os.environ.get('API_ENVIRONMENT', 'PROD')).strip().upper()
print(API_ENVIRONMENT)

if API_ENVIRONMENT=='PROD':
    #  Production Database
    print('*** PROD ***')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': LIVE_DB_NAME,
            'USER': LIVE_DB_USER,
            'PASSWORD': LIVE_DB_PASSWORD,
            'HOST': LIVE_DB_HOST,
            'PORT': LIVE_DB_PORT,
        }
    }
elif API_ENVIRONMENT=='LOCAL':
    # Test Environment Database
    print('*** TEST/LOCAL ***')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': TEST_DB_NAME,
            'USER': TEST_DB_USER,
            'PASSWORD': TEST_DB_PASSWORD,
            'HOST': TEST_DB_HOST,
            'PORT': TEST_DB_PORT,
        }
    }
elif API_ENVIRONMENT=='DOCKER':
    # Docker Environment Database
    print('*** DOCKER ***')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DOCK_DB_NAME,
            'USER': DOCK_DB_USER,
            'PASSWORD': DOCK_DB_PASSWORD,
            'HOST': DOCK_DB_HOST,
            'PORT': DOCK_DB_PORT,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# mjw - lots of these have been adjusted for whitenoise:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# mjw - necessary to get collect static to look in broker data static directory
STATICFILES_DIRS = []

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
