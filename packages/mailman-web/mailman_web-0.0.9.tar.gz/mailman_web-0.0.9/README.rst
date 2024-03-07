=============
Mailman Web
=============

This is a Django project that contains default settings and url settings for
Mailman 3 Web Interface. It consists of the following sub-projects:

* Postorius
* Hyperkitty

Install
=======

To install this project, you run::

  $ pip install mailman-web

If you want to install the latest development version from Git, run::

  $ pip install git+https://gitlab.com/mailman/mailman-web


Changelog
=========

0.0.9 (2024-xx-xx)
~~~~~~~~~~~~~~~~~~

* A spurious warning that ``DJANGO_SETTINGS_MODULE`` and ``MAILMAN_WEB_CONFIG``
  are both set in the environment is no longer issued.  (Closes #25)
* Paths in urls.py are reordered to avoid redirecting ``mailman3/`` and
  ``archives/`` URLs to ``postorius/`` and ``hyperkitty/`` respectively.
 
0.0.8 (2023-10-22)
~~~~~~~~~~~~~~~~~~

* Bump min version dependency on django-mailman3, which will clear all existing
  django sessions so that changes in session serializer doesn't cause errors.
  
0.0.7 (2023-10-21)
~~~~~~~~~~~~~~~~~~

* [**BREAKING**] Reduce the default no. of workers for qrunner to 2. (Fixes #17)
* [**BREAKING**] Due to change in Django's ``SESSION_SERIALIZER``, it will cause
  all existing sessions to cause 500 errors, unless they are removed from the
  database. To do that, you can upgrade to django-mailman3 1.3.10, which will
  remove all current sessions. (See !25)
* Add a new settings module ``mailman_web.settings.dev`` for development purposes.
  To use this, you can run ``export DJANGO_SETTINGS_MODULE=mailman_web.settings.dev``
  and then run ``mailman-web`` commands for dev purposes.
* Min Python version has been upgraded to 3.9 since the same is required for Core.
* Print a warning if a user sets both ``DJANGO_SETTINGS_MODULE`` and ``MAILMAN_WEB_CONFIG``
  as the former overrides the latter. (Fixes #7)
* Migrate to using pyproject.toml and PDM for mailman-web.
  
Fixes
-----
* Instead of overriding ``PYTHONPATH`` env var always, append to it if it has
  already been defined. (Fixes #19)


Project details
===============

* Project home: https://gitlab.com/mailman/mailman-web
* Report bugs at: https://gitlab.com/mailman/mailman-web/-/issues
* Documentation: https://mailman-web.readthedocs.io/en/latest/
* Mailman Documentation: https://docs.mailman3.org


License
=======

Mailman suite is licensed under the
`GNU GPL v3.0 or later (GPLv3+) <http://www.gnu.org/licenses/gpl-3.0.html>`_

Copyright (C) 2020 by the Free Software Foundation, Inc.
