# -*- coding: utf-8 -*-

# Copyright 2014 The Arobito Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Tests for the :py:mod:`ControllerBackend <arobito.controlinterface.ControllerBackend>` module.
"""

import unittest
from arobito.controlinterface.ControllerBackend import App

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


def create_app(test: unittest.TestCase) -> App:
    app = App()
    test.assertIsNotNone(app)
    test.assertIsInstance(app, App)
    return app


class AppAuth(unittest.TestCase):
    """
    Test the :py:meth:`App.auth <arobito.controlinterface.ControllerBackend.App.auth>` method.
    """

    def __check_response_basics(self, response: dict) -> None:
        """
        Check basic response characteristics

        :param response: The response from the auth method call
        """

        self.assertIsNotNone(response, 'Result for req OK is None')
        self.assertIsInstance(response, dict, 'Result is not a dict')
        self.assertIn('auth', response, 'Result does not contain auth element')
        res_auth = response['auth']
        self.assertIn('success', res_auth, 'Result does not contain success element')
        self.assertIsInstance(res_auth['success'], bool, 'Success is not boolean')
        self.assertIn('status', res_auth, 'Result does not contain status element')
        self.assertIsInstance(res_auth['status'], str, 'Status is not a String')

    def __check_success_response(self, response: dict) -> None:
        """
        Check if the response is a success one

        :param response: The response from the auth method call
        """

        self.__check_response_basics(response)

        res_auth = response['auth']
        self.assertTrue(res_auth['success'], 'Success is not true')
        self.assertEqual(res_auth['status'], 'Login successful', 'Status message wrong')
        self.assertIn('key', res_auth, 'Result does not contain a key element')
        self.assertIsInstance(res_auth['key'], str, 'Key is not a String')
        self.assertRegex(res_auth['key'], '^[a-zA-Z0-9]{64}$', 'Key looks not like expected')

    def __check_failed_response(self, response: dict) -> None:
        """
        Check if the response is a failing one

        :param response: The response from the auth method call
        """

        self.__check_response_basics(response)

        res_auth = response['auth']
        self.assertFalse(res_auth['success'], 'Success is not false')
        self.assertEqual(res_auth['status'], 'failed', 'Status message wrong')
        self.assertIn('reason', res_auth, 'Reason is missing')
        self.assertIsInstance(res_auth['reason'], str, 'Reason is not a String')
        self.assertEqual(res_auth['reason'], 'User unknown or password wrong', 'Reason message wrong')

    def runTest(self) -> None:
        """
        Try to use the auth method with working credentials and with wrong credentials.
        """

        request_ok = dict(username='arobito', password='arobito')
        request_wrong_pass = dict(username='arobito', password='wrong_password')
        request_wrong_user = dict(username='wrong_username', password='arobito')
        request_empty = dict()
        request_invalid = dict(invalid='invalid')

        app = create_app(self)

        # Request with None
        self.assertRaises(ValueError, app.auth, None)

        # Request with bad object
        self.assertRaises(ValueError, app.auth, list())

        # Request with working credentials
        response = app.auth(request_ok)
        self.__check_success_response(response)

        # Request with wrong password
        response = app.auth(request_wrong_pass)
        self.__check_failed_response(response)

        # Request with wrong user
        response = app.auth(request_wrong_user)
        self.__check_failed_response(response)

        # Request with empty object
        response = app.auth(request_empty)
        self.__check_failed_response(response)

        # Request with invalid object
        response = app.auth(request_invalid)
        self.__check_failed_response(response)
