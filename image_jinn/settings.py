"""
Django settings for image_jinn project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path


def env(name, default=None):
    return os.environ.get(name, default)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", "not-so-secret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", "0") == "1"

ALLOWED_HOSTS = str(env("ALLOWED_HOSTS")).split(", ")
CORS_ALLOW_ALL_ORIGINS = env("CORS_ALLOW_ALL_ORIGINS", "0") == "1"
CORS_ALLOWED_ORIGINS = str(env("CORS_ALLOWED_ORIGINS")).split(", ")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    # Custom apps
    "apps.images",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "image_jinn.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "image_jinn.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DEFAULT_DB = str(os.path.join(BASE_DIR, "db.sqlite3"))

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": env("DATABASE_NAME", DEFAULT_DB),
        "USER": env("DATABASE_USER", "postgres"),
        "HOST": env("DATABASE_HOST", "localhost"),
        "PORT": env("DATABASE_PORT", 5432),
        "PASSWORD": env("DATABASE_PASSWORD", "postgres"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF config
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# Swagger/OpenAPI
SPECTACULAR_SETTINGS = {
    "TITLE": "Image Jinn",
    "DESCRIPTION": "High-performance image storage service",
    "VERSION": "1.0.0",
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
}

# AWS
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", "minioadmin")
AWS_BUCKET_NAME = env("AWS_BUCKET_NAME", "bucket")
AWS_BUCKET_REGION = env("AWS_BUCKET_REGION", "ap-south-1")
AWS_EXPIRY = 604700
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", "http://127.0.0.1:9000")
AWS_S3_ADDRESSING_STYLE = env("AWS_S3_ADDRESSING_STYLE")

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL", "redis://127.0.0.1:6379")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
