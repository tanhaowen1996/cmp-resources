"""
Django settings for cloud_resources project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j(6isa((3ez0gmwkv@n9)h6n_#k&_6%%t#fgsy(%2p-83b(b3h'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = bool(int(os.getenv('DEBUG', 1)))


# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']
APPEND_SLASH = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'cloud_resources',
    'rest_framework',
    'Virtual',
    'Physical',
]

REST_FRAMEWORK = {
    'DATE_FORMAT': '%Y-%m-%d',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cloud_resources.urls'
HEALTH_CHECK_PATH = os.getenv('HEALTH_CHECK_PATH', '/health')
URL = os.getenv("URL", "127.0.0.1:8080")
WEB_PORT = os.getenv("WEB_PORT", 8080)

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

WSGI_APPLICATION = 'cloud_resources.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'resource'),
        'USER': os.getenv('DB_USER', 'resource'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'resource'),
        # 'PASSWORD': os.getenv('DB_PASSWORD', '4da5fe522058ca244f93257c452f9e9ce27482ab'),
        # 'HOST': os.getenv('DB_HOST', '10.208.0.46'),
        'HOST': os.getenv('DB_HOST', '10.208.224.79'),
        'PORT': int(os.getenv('DB_PORT', 5432)),
        'CONN_MAX_AGE': 3
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i:s'

DATE_FORMAT = 'Y-m-d'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ONEFS_URL = os.getenv('ONEFS_URL', 'https://10.1.51.203:8080/')
ONEFS_USER = os.getenv('ONEFS_USER', 'admin')
ONEFS_PASSWORD = os.getenv('ONEFS_PASSWORD', 'admin')
NFS_ROOT = os.getenv('NEF_ROOT', '/ifs/')
NFS_IP = os.getenv('NFS_IP', 'nasfz.yonghui.cn')
# vsphere list ['USER PASSWORD HOST PORT']
VSPHERE = os.getenv('VSPHERE', ['yhcmp@yhcmpvc7-dev.local m#ss9ttm2E 10.209.1.254 443'])
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=84889afd-ea6a-49fb-b922-72cc10e99629')


SWAGGER = bool(int(os.getenv('SWAGGER', 1)))

# if SWAGGER:
#     SWAGGER_SETTINGS = {
#         'LOGOUT_URL': '/admin/login/',
#         'SECURITY_DEFINITIONS': {
#             OS_TOKEN_KEY: {
#                 'type': 'apiKey',
#                 'name': OS_TOKEN_KEY.lower(),
#                 'in': 'header'
#             },
#             IS_PLATFORM: {
#                 'type': 'apiKey',
#                 'name': IS_PLATFORM.lower(),
#                 'in': 'header'
#             },
#             PROJECTID: {
#                 'type': 'apiKey',
#                 'name': PROJECTID.lower(),
#                 'in': 'header'
#             },
#             REGION: {
#                 'type': 'apiKey',
#                 'name': REGION.lower(),
#                 'in': 'header'
#             }
#         },
#     }
