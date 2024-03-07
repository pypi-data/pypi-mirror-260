# Copyright (C) 2023 by the Free Software Foundation, Inc.
#
# This file is part of mailman-web.
#
# mailman-web is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# mailman-web is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailman-web.  If not, see <http://www.gnu.org/licenses/>.

"""Test basic server startup."""
from django.test import TestCase
from django.contrib.auth.models import User


class SanityTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.su = User.objects.create_superuser(
            'aperson', 'myemail@example.com', 'password')
        self.user = User.objects.create_user(
            'bperson', 'bee@example.com', 'password')

    # def test_basic_postorius(self):
    #     response = self.client.get('/', follow=True)
    #     assert response.status_code == 200

    def _test_endpoints(self, endpoint, as_admin=False, as_user=False):
        if as_admin:
            self.client.force_login(self.su)
        elif as_user:
            self.client.force_login(self.user)

        response = self.client.get(endpoint, follow=True)
        assert response.status_code == 200
        self.client.logout()

    def test_basic_hyperkitty(self):
        self._test_endpoints('/archives')
        self._test_endpoints('/archives', as_user=True)

    def test_basic_django(self):
        self._test_endpoints('/admin')
