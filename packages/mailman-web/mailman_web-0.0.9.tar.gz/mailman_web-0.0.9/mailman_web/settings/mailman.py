#: Mailman Core default API Path
MAILMAN_REST_API_URL = 'http://localhost:8001'
#: Mailman Core API user
MAILMAN_REST_API_USER = 'restadmin'
#: Mailman Core API user's password.
MAILMAN_REST_API_PASS = 'restpass'
#: Mailman Core Shared archiving key. This value is set in the :
#: mailman-hyperkitty's configuration file.
MAILMAN_ARCHIVER_KEY = 'SecretArchiverAPIKey'
#: Host for Mailman Core, from where Hyperkitty will accept connections
#: for archiving.
MAILMAN_ARCHIVER_FROM = ('127.0.0.1', '::1')

#: Base URL where Django/Mailman-web would be listening for requests. Used by
#: Mailman Core for fetching templates.
POSTORIUS_TEMPLATE_BASE_URL = 'http://localhost:8000'

#: Use gravatar in HyperKitty and Postorius.
#: If disabled django_gravatar can be removed from INSTALLED_APPS:
#: INSTALLED_APPS.remove('django_gravatar')
HYPERKITTY_ENABLE_GRAVATAR = True

#: Filter visible Mailing Lists based on the current host being used to serve.
FILTER_VHOST = False

#: Sender in Emails sent out by Postorius.
DEFAULT_FROM_EMAIL = 'postorius@localhost'


#: Django Allauth
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True

#: Protocol for URLs generated for authentication, like email
#: confirmation.
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"


#: Extra configuration for Social auth. For these configuration to be used.
#: each of the social account providers must be first added in INSTALLED_APPS.
#: See :py:data:`mailman_web.settings.base.INSTALLED_APPS` for more
#: configuration.
SOCIALACCOUNT_PROVIDERS = {
    'openid': {
        'SERVERS': [
            dict(id='yahoo',
                 name='Yahoo',
                 openid_url='http://me.yahoo.com'),
        ],
    },
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email'],
        'FIELDS': [
            'email',
            'name',
            'first_name',
            'last_name',
            'locale',
            'timezone',
        ],
        'VERSION': 'v2.4',
    },
}


#: django-compressor
#: https://pypi.python.org/pypi/django_compressor
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sassc -t compressed {infile} {outfile}'),
    ('text/x-sass', 'sassc -t compressed {infile} {outfile}'),
)


# Social auth
#
#: Authentication backends for Django to be used.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

#
# Full-text search engine
#
#: Django-Haystack connection parameters.
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': "fulltext_index",
        # You can also use the Xapian engine, it's faster and more accurate,
        # but requires another library.
        # http://django-haystack.readthedocs.io/en/v2.4.1/installing_search_engines.html#xapian
        # Example configuration for Xapian:
        # 'ENGINE': 'xapian_backend.XapianEngine'
    },
}


# Asynchronous tasks
#
#: Django Q connection parameters.
Q_CLUSTER = {
    'retry': 360,
    'timeout': 300,
    'save_limit': 100,
    'orm': 'default',
    'workers': 2,
}

#: On a production setup, setting COMPRESS_OFFLINE to True will bring a
#: significant performance improvement, as CSS files will not need to be
#: recompiled on each requests. It means running an additional "compress"
#: management command after each code upgrade.
#: http://django-compressor.readthedocs.io/en/latest/usage/#offline-compression
COMPRESS_OFFLINE = True

# Needed for debug mode
# INTERNAL_IPS = ('127.0.0.1',)
