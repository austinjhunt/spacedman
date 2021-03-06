"""
Django settings for spacedrepetition project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY','')
PRODUCTION = int(os.environ.get('PRODUCTION', '0'))
DEBUG = True
BASE_UNIT = 'days'

# AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID','')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY','') 
AWS_LAMBDA_DATA_UPDATE_ARN = os.environ.get('AWS_LAMBDA_DATA_UPDATE_ARN','')
AWS_LAMBDA_API_GATEWAY_URL = os.environ.get('AWS_LAMBDA_API_GATEWAY_URL','')
if PRODUCTION:
    # Force SSL 
    SECURE_SSL_REDIRECT = True



ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1',
    'fie2021-spaced-repetition.herokuapp.com'
] 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'httpsrv'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spacedrepetition.urls'

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
                'httpsrv.context.context'
            ],
        },
    },
]

WSGI_APPLICATION = 'spacedrepetition.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME',''),
        'USER': os.environ.get('DB_USER',''),
        'PASSWORD': os.environ.get('DB_PASSWORD',''),
        'HOST': os.environ.get('DB_HOST',''),
        'PORT': os.environ.get('DB_PORT',''),
    }
}

import django_heroku
# This will override database settings if you provide 
# the heroku environment variable DATABASE_URL in the environment
# Activate Django-Heroku.
django_heroku.settings(locals())


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/' 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
LOGIN_REDIRECT_URL = '/courses' 


# FOR PASSWORD RESET 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '') 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD','') 
EMAIL_USE_TLS = True

# AWS API ENDPOINTS
CREATE_QUESTION_ENDPOINT = AWS_LAMBDA_API_GATEWAY_URL + '/create_question'
RENDER_QUESTION_ENDPOINT = AWS_LAMBDA_API_GATEWAY_URL + '/render_question'
GET_ANSWER_ENDPOINT = AWS_LAMBDA_API_GATEWAY_URL + '/get_answer'
CHECK_ANSWER_ENDPOINT = AWS_LAMBDA_API_GATEWAY_URL + '/check_answer'
