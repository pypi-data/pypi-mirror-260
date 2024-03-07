# -*- coding: utf-8 -*-
# Copyright (C) 2023 by the Free Software Foundation, Inc.
#
# This file is part of mailman-web.
#
# mailman-web is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# mailman-web is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# mailman-web.  If not, see <http://www.gnu.org/licenses/>.
"""
WSGI config for Mialman-web

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from mailman_web.manage import setup

setup()
application = get_wsgi_application()
