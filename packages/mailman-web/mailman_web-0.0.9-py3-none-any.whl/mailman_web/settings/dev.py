import string
import random

from mailman_web.settings.base import *      # noqa: F401,F403
from mailman_web.settings.mailman import *      # noqa: F401,F403


def gen_random():
    """Generate a random secret key for dev workflow."""
    return ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=20))


# A randomly generated secret key. This is not needed to be random, but meh.
SECRET_KEY = gen_random()
DEBUG = True

# Needed for debug mode
INTERNAL_IPS = ('127.0.0.1',)

# Allowed_hosts.
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '::1',
    ]

# Use console backend as default so all the sent out emails
# are printed to stdout.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
