#!/usr/bin/env python
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
import os
import sys
from pathlib import Path


def setup():
    """Setup environment for Mailman web."""
    django_settings = os.getenv('DJANGO_SETTINGS_MODULE', None)
    MAILMAN_WEB_CONFIG = os.getenv('MAILMAN_WEB_CONFIG', None)
    if django_settings is not None:
        # If the user has set DJANGO_SETTINGS_MODULE, then don't
        # do anything and return.
        if MAILMAN_WEB_CONFIG is not None:
            print('WARNING: "DJANGO_SETTINGS_MODULE" and "MAILMAN_WEB_CONFIG"'
                  ' environment variables are both set. DJANGO_SETTINGS_MODULE'
                  ' is being used and MAILMAN_WEB_CONFIG is ignored.',
                  file=sys.stderr)
        return

    MAILMAN_WEB_CONFIG = os.getenv(
        'MAILMAN_WEB_CONFIG',
        '/etc/mailman3/settings.py',
    )

    if not os.path.exists(MAILMAN_WEB_CONFIG):
        print('Mailman web configuration file at {} does not exist'.format(
              MAILMAN_WEB_CONFIG), file=sys.stderr)
        print('Modify "MAILMAN_WEB_CONFIG" environment variable to point at '
              'settings.py or set "DJANGO_SETTINGS_MODULE".', file=sys.stderr)
        if len(sys.argv) > 1 and sys.argv[1] == 'help':
            os.environ['DJANGO_SETTINGS_MODULE'] = 'mailman_web.settings'
            import mailman_web.settings
            mailman_web.settings.SECRET_KEY = 'only_set_here_for_help_cmd'
        else:
            sys.exit(1)
    else:
        config_path = Path(MAILMAN_WEB_CONFIG).resolve()
        add_to_pythonpath(str(config_path.parent))
        os.environ['DJANGO_SETTINGS_MODULE'] = config_path.stem


def add_to_pythonpath(value):
    """Add the settings file's parent dir to Python's PATH."""
    # Add to sys.path, so that the imports following after this
    # method run will work.
    sys.path.append(value)
    # Finally, also add to PYTHONPATH so if there are any re-execs
    # then it is carried over. It is found in Django commands that
    # such things can occur.
    existing_path = os.environ.get('PYTHONPATH')
    if existing_path is None:
        os.environ['PYTHONPATH'] = value
        return
    # If the PYTHONPATH has been set for some other reason
    # not override it, instead append to it.
    # os.pathsep is used for separating entries in PYTHONPATH, same as
    # PATH.
    os.environ['PYTHONPATH'] = f'{existing_path}{os.pathsep}{value}'
    print(
        'Updated PYTHONPATH to : {}'.format(os.environ.get('PYTHONPATH')),
        file=sys.stderr
        )


def main():
    setup()

    os.environ['DJANGO_IS_MANAGEMENT_COMMAND'] = '1'
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
