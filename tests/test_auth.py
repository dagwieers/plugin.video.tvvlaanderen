# -*- coding: utf-8 -*-
""" Tests for Auth API """

# pylint: disable=missing-docstring,no-self-use

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import random
import string
import unittest

from resources.lib import kodiutils
from resources.lib.solocoo.auth import AuthApi, AccountStorage
from resources.lib.solocoo.exceptions import InvalidLoginException

_LOGGER = logging.getLogger(__name__)


@unittest.skipUnless(kodiutils.get_setting('username') and kodiutils.get_setting('password'), 'Skipping since we have no credentials.')
class TestAuth(unittest.TestCase):

    def test_login(self):
        auth = AuthApi(kodiutils.get_setting('username'),
                       kodiutils.get_setting('password'),
                       kodiutils.get_setting('tenant'),
                       kodiutils.get_tokens_path())

        account = auth.get_tokens()
        self.assertIsInstance(account, AccountStorage)

        devices = auth.list_devices()
        self.assertIsInstance(devices, dict)

        entitlements = auth.list_entitlements()
        self.assertIsInstance(entitlements, dict)

    # def test_anonymous(self):
    #     auth = AuthApi('',
    #                    '',
    #                    kodiutils.get_setting('tenant'),
    #                    kodiutils.get_tokens_path())
    #     account = auth.get_tokens()
    #     self.assertIsInstance(account, AccountStorage)

    def test_errors(self):
        with self.assertRaises(InvalidLoginException):
            AuthApi(self._random_email(), 'test', 'tvv', token_path=kodiutils.get_tokens_path())

    @staticmethod
    def _random_email(domain='gmail.com'):
        """ Generate a random e-mail address. """
        return '%s@%s' % (''.join(random.choice(string.ascii_letters) for i in range(12)), domain)


if __name__ == '__main__':
    unittest.main()
