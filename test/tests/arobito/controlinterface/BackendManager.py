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
        self.assertIn('username', user_object, 'User name is not in the user object')
        self.assertEqual(user_object['username'], 'arobito', 'User name in user object is not "arobito"')
        self.assertIn('level', user_object, 'User level is not in user object')
        self.assertEqual(user_object['level'], 'Administrator', 'User level is not "Administrator"')
        self.assertIn('timestamp', user_object, 'Timestamp is not in user object')
        self.assertIn('last_access', user_object, 'Last access timestamp is not in user object')
        self.assertIsInstance(user_object['timestamp'], float, 'Timestamp is not a float')
        self.assertIsInstance(user_object['last_access'], float, 'Last access is not a float')
        self.assertTrue(user_object['timestamp'] <= user_object['last_access'],
                        'Timestamp is not less or equal the last access')

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


class SessionManagerLogin(unittest.TestCase):
    """
    Test the method :py:meth:`login <arobito.controlinterface.BackendManager.SessionManager.login>` from class
    :py:class:`SessionManager <arobito.controlinterface.BackendManager.SessionManager>`.

    It works only with the standard settings of the ``controller.ini`` file.
    """

    def runTest(self):
        """
        Try to use the login
        """

        session_manager = SessionManager()
        self.assertIsNotNone(session_manager, 'Session Manager is None')

        # Correct credentials
        key = session_manager.login('arobito', 'arobito')
        self.assertIsNotNone(key, 'Key is None')
        self.assertIsInstance(key, str, 'Key is not a String')


class SessionManagerLogout(unittest.TestCase):
    """
    Test the method :py:meth:`logout <arobito.controlinterface.BackendManager.SessionManager.logout>` from class
    :py:class:`SessionManager <arobito.controlinterface.BackendManager.SessionManager>`.

    It works only with the standard settings of the ``controller.ini`` file.
    """

    def runTest(self):
        pass


class SessionManagerCleanup(unittest.TestCase):
    """
    Test the method :py:meth:`cleanup <arobito.controlinterface.BackendManager.SessionManager.cleanup>` from class
    :py:class:`SessionManager <arobito.controlinterface.BackendManager.SessionManager>`.

    It works only with the standard settings of the ``controller.ini`` file.
    """

    def runTest(self):
        """
        Just make sure that there is no exception happening when this method is called.

        During our tests, there will be not enough time to let sessions expire. This is definitely a gap in our tests.
        """
        session_manager = SessionManager()
        session_manager.cleanup()


class SessionManagerGetCurrentSessions(unittest.TestCase):
    """
    Test the method :py:meth:`get_current_sessions
    <arobito.controlinterface.BackendManager.SessionManager.get_current_sessions>` from class :py:class:`SessionManager
    <arobito.controlinterface.BackendManager.SessionManager>`.

    It works only with the standard settings of the ``controller.ini`` file.
    """

    def runTest(self):
        pass


class SessionManagerGetUser(unittest.TestCase):
    """
    Test the method :py:meth:`get_user <arobito.controlinterface.BackendManager.SessionManager.get_user>` from class
    :py:class:`SessionManager <arobito.controlinterface.BackendManager.SessionManager>`.

    It works only with the standard settings of the ``controller.ini`` file.
    """

    def runTest(self):
        pass


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
