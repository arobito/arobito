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
from arobito.controlinterface.BackendManager import UserManager

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class UserManagerGetUserByUsernameAndPassword(unittest.TestCase):
    """
    Test the method :py:meth:`get_user_by_username_and_password
    <arobito.controlinterface.BackendManager.UserManager.get_user_by_username_and_password` from class
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
        self.assertEqual(user_object['timestamp'], user_object['last_access'],
                         'Timestamp and last access are not equal')

        # And some wrong stuff
        user_object = user_manager.get_user_by_username_and_password('arobito', 'wrong_password')
        self.assertIsNone(user_object, 'The user should be None, but isn\'t')

        # And some more wrong stuff
        user_object = user_manager.get_user_by_username_and_password('wrong_username', 'arobito')
        self.assertIsNone(user_object, 'The user should be None, but isn\'t')

        # And everything wrong stuff
        user_object = user_manager.get_user_by_username_and_password('wrong_username', 'wrong_password')
        self.assertIsNone(user_object, 'The user should be None, but isn\'t')
