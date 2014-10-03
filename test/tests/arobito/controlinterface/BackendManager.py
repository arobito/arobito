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
Tests for the :py:mod:`BackendManager <arobito.controlinterface.BackendManager>` module.
"""

import unittest
from arobito.controlinterface.BackendManager import UserManager, SessionManager

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


def evaluate_user_object(test: unittest.TestCase, user_object: dict) -> None:
    """
    Helper function for evaluating an user object

    :param test: The currently running test case
    :param user_object: The user object to evaluate
    """
    test.assertIn('username', user_object, 'User name is not in the user object')
    test.assertEqual(user_object['username'], 'arobito', 'User name in user object is not "arobito"')
    test.assertIn('level', user_object, 'User level is not in user object')
    test.assertEqual(user_object['level'], 'Administrator', 'User level is not "Administrator"')
    test.assertIn('timestamp', user_object, 'Timestamp is not in user object')
    test.assertIn('last_access', user_object, 'Last access timestamp is not in user object')
    test.assertIsInstance(user_object['timestamp'], float, 'Timestamp is not a float')
    test.assertIsInstance(user_object['last_access'], float, 'Last access is not a float')
    test.assertTrue(user_object['timestamp'] <= user_object['last_access'],
                    'Timestamp is not less or equal the last access')


class UserManagerGetUserByUsernameAndPassword(unittest.TestCase):
    """
    Test the method :py:meth:`get_user_by_username_and_password
    <arobito.controlinterface.BackendManager.UserManager.get_user_by_username_and_password>` from class
    :py:class:`UserManager <arobito.controlinterface.BackendManager.UserManager>`.

    It works only with the standard settings of the ``users.ini`` file.
    """

    def runTest(self) -> None:
        """
        Just try to get user data by the default settings.
        """

        user_manager = UserManager()
        self.assertIsNotNone(user_manager, 'Cannot create an instance of the UserManager')

        # Correct credentials
        user_object = user_manager.get_user_by_username_and_password('arobito', 'arobito')
        self.assertIsNotNone(user_object, 'Did not received a user object')
        self.assertIsInstance(user_object, dict, 'User object is not a dict')

        # Is all in there what we need?
        evaluate_user_object(self, user_object)

        # And some wrong stuff
        user_object = user_manager.get_user_by_username_and_password('arobito', 'wrong_password')
        self.assertIsNone(user_object, 'The user should be None, but isn\'t')

        # And some more wrong stuff
        user_object = user_manager.get_user_by_username_and_password('wrong_username', 'arobito')
        self.assertIsNone(user_object, 'The user should be None, but isn\'t')

        # And everything wrong stuff
        user_object = user_manager.get_user_by_username_and_password('wrong_username', 'wrong_password')
        self.assertIsNone(user_object, 'The user should be None, but isn\'t')


class UserManagerIsSingleton(unittest.TestCase):
    """
    Find out if the :py:class:`UserManager <arobito.controlinterface.BackendManager.UserManager>` is created as
    singleton.
    """

    def runTest(self):
        """
        Simply create two instances of :py:class:`UserManager <arobito.controlinterface.BackendManager.UserManager>` and
        compare them.
        """

        user_manager1 = UserManager()
        user_manager2 = UserManager()
        self.assertIsNotNone(user_manager1, 'User Manager 1 is None')
        self.assertIsNotNone(user_manager2, 'User Manager 2 is None')
        self.assertEqual(user_manager1, user_manager2, 'User Manager objects are not equal')


class SessionManagerMultiTest(unittest.TestCase):
    """
    Test the :py:class:`SessionManager <arobito.controlinterface.BackendManager.SessionManager>` class.

    It works only with the standard settings of the ``controller.ini`` file.
    """

    def __check_count(self, count: int, expected: int) -> None:
        self.assertIsNotNone(count, 'Count is None')
        self.assertIsInstance(count, int, 'Count is not Integer')
        self.assertEqual(count, expected, 'Count is not {:d}'.format(expected))

    def runTest(self) -> None:
        """
        Simulate a complete workflow through the class' methods
        """

        session_manager = SessionManager()
        self.assertIsNotNone(session_manager, 'Session Manager is None')

        # There should be no active session
        session_count = session_manager.get_current_sessions()
        self.__check_count(session_count, 0)

        # Correct credentials
        key_correct = session_manager.login('arobito', 'arobito')
        self.assertIsNotNone(key_correct, 'Key is None')
        self.assertIsInstance(key_correct, str, 'Key is not a String')
        self.assertRegex(key_correct, '^[a-zA-Z0-9]{64}$', 'Key does not match expectations')

        # Count should be 1 now
        session_count = session_manager.get_current_sessions()
        self.__check_count(session_count, 1)

        # Incorrect credentials
        key_invalid = session_manager.login('arobito', 'wrong_password')
        self.assertIsNone(key_invalid, 'Invalid key produced')

        # Count should be still 1
        session_count = session_manager.get_current_sessions()
        self.__check_count(session_count, 1)

        # Call cleanup explicitly
        session_manager.cleanup()

        # Count should be still 1
        session_count = session_manager.get_current_sessions()
        self.__check_count(session_count, 1)

        # Try logout - with invalid key
        session_manager.logout('invalid_key')

        # Count should be still 1
        session_count = session_manager.get_current_sessions()
        self.__check_count(session_count, 1)

        # Logout with the working key
        session_manager.logout(key_correct)

        # Count should now be 0
        session_count = session_manager.get_current_sessions()
        self.__check_count(session_count, 0)

        # Login loop
        key_list = list()
        for i in range(0, 1000):
            key = session_manager.login('arobito', 'arobito')
            self.assertIsNotNone(key, 'Key in loop run {:d} is None'.format(i))
            self.assertIsInstance(key, str, 'Key in loop run {:d} is not a String'.format(i))
            self.assertRegex(key, '^[a-zA-Z0-9]{64}$', 'Key in loop run does not match expectations'.format(i))
            key_list.append(key)
            session_count = session_manager.get_current_sessions()
            self.__check_count(session_count, i)

        self.assertEqual(len(key_list), 1000, 'Key list is not of the size expected')

        # Logout loop
        for i in range(1000, 0, -1):
            session_manager.logout(key_list.pop())
            session_count = session_manager.get_current_sessions()
            self.__check_count(session_count, i - 1)

        self.assertEqual(len(key_list), 0, 'Key list is not of the size expected')

        # Count should now be 0
        session_count = session_manager.get_current_sessions()
        self.__check_count(session_count, 0)

        # Create a key for the next tests (redundant to the tests above)
        key = session_manager.login('arobito', 'arobito')
        self.assertIsNotNone(key, 'Key is None')
        self.assertIsInstance(key, str, 'Key is not a String')
        self.assertRegex(key, '^[a-zA-Z0-9]{64}$', 'Key does not match expectations')

        # Try to get an invalid user
        user_object = session_manager.get_user('invalid_session')
        self.assertIsNone(user_object, 'Invalid user fetched')

        # Get a user object from a session
        user_object = session_manager.get_user(key)
        self.assertIsNotNone(user_object, 'User object is None')
        self.assertIsInstance(user_object, dict, 'User object is not a dict')

        # Count should now be 1
        session_count = session_manager.get_current_sessions()
        self.__check_count(session_count, 1)

        # Evaluate the user object returned
        evaluate_user_object(self, user_object)


class SessionManagerIsSingleton(unittest.TestCase):
    """
    Find out if the :py:class:`SessionManager <arobito.controlinterface.BackendManager.SessionManager>` is created as
    singleton.
    """

    def runTest(self):
        """
        Simply create two instances of :py:class:`UserManager <arobito.controlinterface.BackendManager.SessionManager>`
        and compare them.
        """

        session_manager1 = SessionManager()
        session_manager2 = SessionManager()
        self.assertIsNotNone(session_manager1, 'Session Manager 1 is None')
        self.assertIsNotNone(session_manager2, 'Session Manager 2 is None')
        self.assertEqual(session_manager1, session_manager2, 'Session Manager objects are not equal')
