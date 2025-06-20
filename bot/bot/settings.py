"""
Django settings for bot project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
import corsheaders
from corsheaders.defaults import default_headers

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-_)=qk!+dh_#-!%)hi3*4pnl5f^k#eyzndwp9sx^azg1-duz)sf')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', "aws-0-eu-central-1.pooler.supabase.com,localhost,127.0.0.1,3490-156-217-3-147.ngrok-free.app").split(',')]
#ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(',')
ALLOWED_HOSTS=["aws-0-eu-central-1.pooler.supabase.com","localhost","127.0.0.1","13ab-156-214-196-78.ngrok-free.app"]

# Application definition
INSTALLED_APPS = [
    # Third-party apps
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',  # Added for JWT authentication
    'django.contrib.sites',  # Required for allauth
    
    # Allauth core
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Social providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    
    # Custom apps
    'accounts.apps.AccountsConfig',  # Uncommented since AUTH_USER_MODEL references it
    'dashboard.apps.DashboardConfig',
    'conversations.apps.ConversationsConfig',
    'create_agent.apps.CreateAgentConfig',
    'integrations.apps.IntegrationsConfig',
    'usage_plans.apps.UsagePlansConfig',
    
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CSRF_TRUSTED_ORIGINS = ['https://preview--chatty-user-homebase.lovable.app','https://13ab-156-214-196-78.ngrok-free.app']

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Required for allauth
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'https://preview--chatty-user-homebase.lovable.app',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    'ngrok-skip-browser-warning',
    'authorization',  # Allow Authorization header for JWT
    'content-type',
    'accept',
    'origin',
    'x-requested-with',
]


# Note: CORS_ALLOW_ALL_ORIGINS = True overrides CORS_ALLOWED_ORIGINS
# Consider removing this if you want to restrict origins
#CORS_ALLOW_ALL_ORIGINS = True

# ALLOWED_ORIGINS is redundant with CORS_ALLOWED_ORIGINS
# Consider removing this if it's not used elsewhere in the codebase
#ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS.copy()



ROOT_URLCONF = 'bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Added templates directory
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

WSGI_APPLICATION = 'bot.wsgi.application'

# Connect to Supabase via connection pooling

print("Using DB password:", os.getenv("password"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('dbname',),
        'USER': os.getenv('user',),
        'PASSWORD': os.getenv('password',),
        'HOST': os.getenv('host',),
        'PORT': os.getenv('port',),
        'OPTIONS': {
            'sslmode': 'require',
            'client_encoding': 'UTF8',
        },
        'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', '0')),
    }
}

# Cache settings
CACHES = {
    'default': {
        'BACKEND': os.getenv('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': os.getenv('CACHE_LOCATION', 'unique-snowflake'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings
if not DEBUG:
    # Only enable SSL redirect for non-API URLs
    SECURE_SSL_REDIRECT = False  # Changed to False to prevent API redirects
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        # Removed IsAuthenticated to allow unauthenticated access to registration
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
}

# JWT settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}

