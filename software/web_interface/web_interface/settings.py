"""
Django settings for web_interface project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7dn+jianr!9+v(e-zs3*-wybiz#h)4r^+9=_(=*uq0!)fq#t22'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['jeremych.zapto.org', 'sleepify.zapto.org', 'localhost', '127.0.0.1', '192.168.1.100']

# Application definition
INSTALLED_APPS = [
    # my webapps
    'personal',
    'myaccount',
    'MLBlock',
    'newML',
    # 'alpr',
    'daterange_filter',

    # REST API
    'rest_framework',
    'rest_framework.authtoken',

    # rest-auth
    'rest_auth',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.instagram',

    # bootstrap
    'bootstrap3',

    #sphinx docs
    'docs',

    # django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # django defaults
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web_interface.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # django defaults
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'web_interface.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
# List of directories where "./manage.py collectstatic" will look for files, which it puts all together into STATIC_ROOT. Each app that you have can have it's own "static" files directory.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
# This is the "static" files directory where say most of the CSS/JS/IMG files are stored for the project.
)

# Physical system path where the static files are stored. Files that are being uploaded by the user.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# URL that your MEDIA files will be accessible through the browser.
MEDIA_URL = '/media/'

###########################################################################
###########################################################################
###########################################################################
###########################################################################
# all-auth

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 30

# facebook app https://developers.facebook.com/apps/1786476698345753/dashboard/
# twitter app https://apps.twitter.com/app/13427802/keys
# instagram app https://www.instagram.com/developer/clients/1c01f7e2089347fb9a7e9739be3babb6/edit/
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_GB',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4',
    }
}

# spit email stuff into console for now
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# actual email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_HOST_USER = 'jeremych@outlook.com'
EMAIL_HOST_PASSWORD = 'lnqmjyqxucopvxkq'  # get app password, not actual email password
EMAIL_PORT = 587  # 587 gmail
# This did the trick
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

###########################################################################
###########################################################################
###########################################################################
###########################################################################
# rest framework
REST_FRAMEWORK = {
    #'DEFAULT_PERMISSION_CLASSES': [
    #    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    #],
    'FORM_METHOD_OVERRIDE': None,
    'FORM_CONTENT_OVERRIDE': None,
    'FORM_CONTENTTYPE_OVERRIDE': None
}

###########################################################################
###########################################################################
###########################################################################
###########################################################################
# others
CSRF_COOKIE_SECURE = False  # allow transportation of CSRF over HTTP

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/myaccount/profile/'  # It means home view

SITE_ID = 1  # for allauth and django.contrib.sites

BOOTSTRAP3 = {
    'include_jquery': True,
}

SENDFILE_BACKEND = 'sendfile.backends.development'

DOCS_ROOT = os.path.join(BASE_DIR, "docs/_build/html/")
DOCS_ACCESS = 'public'