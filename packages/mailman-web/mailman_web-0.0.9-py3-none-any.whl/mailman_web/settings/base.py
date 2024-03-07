# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.contrib.messages import constants as messages
from pathlib import Path

#: The base directory for logs and database.
BASE_DIR = Path('/opt/mailman/web')

#: Default list of admins who receive the emails from error logging.
ADMINS = (
    ('Mailman Suite Admin', 'root@localhost'),
)

#: Hosts/domain names that are valid for this site; required if DEBUG is False.
#: See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "localhost",  # Archiving API from Mailman, keep it.
    # "lists.your-domain.org",
    # Add here all production URLs you may have.
]

#: Enable Development Mode.
DEBUG = False


#: URL Configuration for Django
ROOT_URLCONF = 'mailman_web.urls'


#: Default list of django applications.
#: Each social account provider is an application and by default no social auth
#: providers are enabled. To enable a social auth provider, you can add them
#: to list of INSTALLED_APPS. For example::
#:
#:     DJANGO_SOCIAL_AUTH_PROVIDERS = [
#:         'allauth.socialaccount.providers.openid',
#:         'django_mailman3.lib.auth.fedora',
#:         'allauth.socialaccount.providers.github',
#:         'allauth.socialaccount.providers.gitlab',
#:         'allauth.socialaccount.providers.google',
#:         'allauth.socialaccount.providers.facebook',
#:         'allauth.socialaccount.providers.twitter',
#:         'allauth.socialaccount.providers.stackexchange',
#:     ]
#:     INSTALLED_APPS += DJANGO_SOCIAL_AUTH_PROVIDERS
#:
#: A full list of providers can be found at
#: https://django-allauth.readthedocs.io/en/latest/providers.html
#: Please also note that extra configuration is required after
#: a provider is enabled. Django-allauth's documentation mentioned
#: above provides more details about how to configure one.
INSTALLED_APPS = [
    'hyperkitty',
    'postorius',
    'django_mailman3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'django_gravatar',
    'compressor',
    'haystack',
    'django_extensions',
    'django_q',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]


#: Default Django Middlewares.
MIDDLEWARE = (
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_mailman3.middleware.TimezoneMiddleware',
    'postorius.middleware.PostoriusMiddleware',
)

#: Default Template finders.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.csrf',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_mailman3.context_processors.common',
                'hyperkitty.context_processors.common',
                'postorius.context_processors.postorius',
            ],
        },
    },
]

#: Wsgi application import path. This will be used by the WSGI server which
#: will be used to deploy this application.
WSGI_APPLICATION = 'mailman_web.wsgi.application'

#: Default Database to be used.
#: Example for PostgreSQL (**recommanded for production**)::
#:
#:    'default': {
#:        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#:        'NAME': 'database_name',
#:        'USER': 'database_user',
#:        'PASSWORD': 'database_password',
#:        'HOST': 'localhost',
#:    }
#:
#: For MySQL/MariaDB also add the following to the the configuration::
#:
#:     'OPTIONS': {'charset': 'utf8mb4'}  # Enable utf8 4-byte encodings.
#:
#: Check out
#: `Django documentation
#: <https://docs.djangoproject.com/en/3.0/ref/settings/#databases>`_ for
#: more details.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'mailman-web.db'),
        'HOST': '',
        'PORT': '',
    }
}

# Maintain type of autogenerated keys going forward
# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


#: Default password validators.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#: Default Language code.
LANGUAGE_CODE = 'en-us'

#: Default timezone.
TIME_ZONE = 'UTC'

#: Enable internationalization.
USE_I18N = True

#: Enable localization.
USE_L10N = True

#: Use the timezone information.
USE_TZ = True


#: Default path where static files will be placed.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#: URL prefix for static files.
#: Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

#: Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # BASE_DIR + '/static/',
)

#: List of finder classes that know how to find static files in
#: various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)


#: Default Django URL to redirect to for Login.
LOGIN_URL = 'account_login'
#: Default Django URL to redirect to after a successful login.
LOGIN_REDIRECT_URL = 'list_index'
#: Default Django URL to Logout the user.
LOGOUT_URL = 'account_logout'

#: If you enable email reporting for error messages, this is where those emails
#: will appear to be coming from. Make sure you set a valid domain name,
#: otherwise the emails may get rejected.
#: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SERVER_EMAIL
SERVER_EMAIL = 'root@localhost.local'

#: The default implementation to send out emails. This can be customized to
#: something else for testing purposes.
#: https://docs.djangoproject.com/en/dev/topics/email/#email-backends
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


#: Default Logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'mailmanweb.log'),
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'hyperkitty': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'postorius': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'q': {
            'level': 'WARNING',
            'propagate': False,
            'handlers': ['console', 'file'],
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(name)s %(message)s'  # noqa: E501
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
}

#: Current Django Site being served. This is used to customize the web host
#: being used to serve the current website. For more details about Django
#: site, see: https://docs.djangoproject.com/en/dev/ref/contrib/sites/
SITE_ID = 1
