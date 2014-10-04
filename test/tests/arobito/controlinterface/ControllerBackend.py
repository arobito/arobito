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
    """
    Create an :py:class:`App <arobito.controlinterface.ControllerBackend.App>` instance

    :param test: The currently running unit test case
    :return: An instance of App
    """

    app = App()
    test.assertIsNotNone(app)
    test.assertIsInstance(app, App)
    return app


def get_valid_key(test: unittest.TestCase, app: App=None) -> str:
    """
    Produce a valid key by using the arobito default credentials against the :py:method:`App.auth
    <arobito.controlinterface.ControllerBackend.App.auth>` method

    :param test: The currently running unit test case
    :return: A valid key
    """
    if app is None:
        app = create_app(test)

    request_valid = dict(username='arobito', password='arobito')
    response = app.auth(request_valid)
    test.assertIsNotNone(response, 'Response is none')
    test.assertIsInstance(response, dict, 'Response is not a dict')
    test.assertIn('auth', response, 'Response does not contain an auth element')
    auth = response['auth']
    test.assertIn('key', auth, 'Auth object does not contain a key')
    key = auth['key']
    test.assertIsNotNone(key, 'Key is None')
    test.assertIsInstance(key, str, 'Key is not a String')
    test.assertRegex(key, '^[a-zA-Z0-9]{64}$', 'Key looks not like expected')
    return key


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
        app.logout(dict(key=response['auth']['key']))

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


class AppLogout(unittest.TestCase):
    """
    Test the :py:meth:`App.logout <arobito.controlinterface.ControllerBackend.App.logout>` method.
    """

    def __check_response(self, response: dict) -> None:
        """
        Verify the response object

        :param response: The response object
        """

        self.assertIsNotNone(response, 'Response is None')
        self.assertIsInstance(response, dict, 'Response is not a dict')
        self.assertIn('logout', response, 'Response does not contain logout element')
        self.assertIsInstance(response['logout'], bool, 'Logout is not boolean')
        self.assertTrue(response['logout'], 'Logout is not true')

    def runTest(self) -> None:
        """
        Test the logout method with real and wrong keys
        """

        app = create_app(self)

        # Request with None
        self.assertRaises(ValueError, app.logout, None)

        # Request with bad object
        self.assertRaises(ValueError, app.logout, list())

        response_wrong = dict(key='wrong_key')
        request_invalid = dict(invalid='invalid')
        request_empty = dict()

        # Invalid request
        response = app.logout(request_invalid)
        self.__check_response(response)

        # Empty request
        response = app.logout(request_empty)
        self.__check_response(response)

        # Wrong request
        response = app.logout(response_wrong)
        self.__check_response(response)

        # For a real test, we need a key, and therefore a auth first
        response = app.logout(dict(key=get_valid_key(self, app)))
        self.__check_response(response)


class AppShutdown(unittest.TestCase):
    """
    Test the :py:meth:`App.shutdown <arobito.controlinterface.ControllerBackend.App.shutdown>` method.
    """

    def runTest(self) -> None:
        """
        Testing the shutdown method would cancel the program, so we can only check the behaviour with bad input.
        """

        app = create_app(self)

        # Request with None
        self.assertRaises(ValueError, app.shutdown, None)

        # Request with bad object
        self.assertRaises(ValueError, app.shutdown, list())

        # Request with invalid key
        response = app.shutdown(dict(key='invalid_key'))

        self.assertIsNotNone(response, 'Response is None')
        self.assertIsInstance(response, dict, 'Response is not a dict')
        self.assertIn('shutdown', response, 'Response does not contain a shutdown element')
        self.assertIsInstance(response['shutdown'], bool, 'Shutdown element is not boolean')
        self.assertFalse(response['shutdown'], 'Shutdown element is not false')


class AppGetSessionCount(unittest.TestCase):
    """
    Test the :py:meth:`App.get_session_count <arobito.controlinterface.ControllerBackend.App.get_session_count>` method.
    """

    def __check_basic_response(self, response: dict) -> None:
        """
        Check the basics of a response objects

        :param response: The response from the get_session_count method
        """

        self.assertIsNotNone(response, 'Response is None')
        self.assertIsInstance(response, dict, 'Response is not a dict')
        self.assertIn('session_count', response, 'Response does not contain session_count element')
        self.assertIsInstance(response['session_count'], int, 'Session Count is not an Integer')

    def __check_invalid_response(self, response: dict) -> None:
        """
        Check an invalid response object

        :param response: The object to check
        """

        self.__check_basic_response(response)
        self.assertEqual(response['session_count'], -1, 'Session count is not -1')

    def __check_valid_response(self, response: dict, expected: int) -> None:
        """
        Check a valid response

        :param response: The object to check
        :param expected: The session count expected
        """

        self.__check_basic_response(response)
        self.assertEqual(response['session_count'], expected, 'Session count is not {:d}'.format(expected))

    def runTest(self) -> None:
        """
        Test the method with bad and valid input
        """

        app = create_app(self)

        # Request with None
        self.assertRaises(ValueError, app.get_session_count, None)

        # Request with bad object
        self.assertRaises(ValueError, app.get_session_count, list())

        # Try with an invalid key
        response = app.get_session_count(dict(key='invalid_key'))
        self.__check_invalid_response(response)

        # Work with valid keys
        master_key = get_valid_key(self, app)
        key_list = list()

        for i in range(0, 10):
            key = get_valid_key(self, app)
            response = app.get_session_count(dict(key=master_key))
            self.__check_valid_response(response, i + 2)
            key_list.append(key)

        for i in range(10, 0, -1):
            key = key_list.pop()
            app.logout(dict(key=key))
            response = app.get_session_count(dict(key=master_key))
            self.__check_valid_response(response, i)

        app.logout(dict(key=master_key))
        self.assertEqual(len(key_list), 0, 'KeyList is not empty')

        response = app.get_session_count(dict(key=master_key))
        self.__check_invalid_response(response)
