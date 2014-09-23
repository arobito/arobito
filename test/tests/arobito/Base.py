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

import unittest
import arobito.Base
import re

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class SingletonMock(object, metaclass=arobito.Base.SingletonMeta):
    """
    A mock class that is meant to be handled as a singleton. It is used by the :py:class:`Singleton <.Singleton>` test
    case.
    """

    def __init__(self):
        self.value = 'After Init'

    def set_value(self, value: str) -> None:
        """
        Set the value
        :param value: The value
        """
        self.value = value

    def get_value(self) -> str:
        """
        Get the value
        :return: The value
        """
        return self.value


class Singleton(unittest.TestCase):
    """
    Test the singleton meta class (:py:class:`SingletonMeta <arobito.Base.SingletonMeta>`)

    Many things within this project rely on a working singleton implementation. It's very important that this behaviour
    is checked in every test run, especially when the language (Python) version changes.
    """

    def runTest(self) -> None:
        """
        Try to create two instances of the singleton (the test uses the :py:class:`SingletonMock <.SingletonMock>`
        class) and tests if values and instances are equal.
        """
        test_string = 'Value set from test ABC123'
        singleton_one = SingletonMock()
        singleton_one.set_value(test_string)
        singleton_two = SingletonMock()
        self.assertEqual(singleton_two.get_value(), test_string, 'Singleton 2 value does not match test string')
        self.assertEqual(singleton_one, singleton_two, 'Singleton 1 and 2 are not equal')
        self.assertEqual(singleton_one.get_value(), singleton_two.get_value(),
                         'The values in Singleton 1 and Singleton 2 are not equal')
        test_string = 'Another value'
        singleton_two.set_value(test_string)
        self.assertEqual(singleton_one.get_value(), test_string, 'Singleton 1 value does not match test string')
        self.assertEqual(singleton_one, singleton_two, 'Singleton 1 and 2 are not equal')
        self.assertEqual(singleton_one.get_value(), singleton_two.get_value(),
                         'The values in Singleton 1 and Singleton 2 are not equal')


class CreateSalt(unittest.TestCase):
    """
    Test the :py:func:`create_salt <arobito.Base.create_salt>` function
    """

    def runTest(self) -> None:
        """
        Create some salts and check the size of the returning string. Check if the string contains the percent sign.
        Also, check the default length explicitly.

        Also checks if the correct error is raised on bad arguments.
        """
        self.assertRaises(ValueError, arobito.Base.create_salt, 0)
        self.assertRaises(ValueError, arobito.Base.create_salt, -1)
        self.assertRaises(ValueError, arobito.Base.create_salt, -100)
        regex = re.compile('^[a-zA-Z0-9\|\^\.,;_\-:<>+\]\[\(\)\$!&=\"\'´`\*@:~\{\}#\?/\\\]+$', re.DOTALL)
        for i in range(1, 1000):
            salt = arobito.Base.create_salt(i)
            self.assertEqual(len(salt), i, 'Length of salt is unexpected')
            self.failIf(regex.match(salt) is None, 'Salt "{:s}" does not match the requirements'.format(salt))
        salt = arobito.Base.create_salt()
        # Checking the length is enough here - all other specifications are checked within the loop above.
        self.assertEqual(len(salt), 128, 'Salt default length wrong')


class CreateSimpleKey(unittest.TestCase):
    """
    Test the :py:func:`create_simple_key <arobito.Base.create_simple_key>` function
    """

    def runTest(self) -> None:
        """
        A simple key contains only numbers and letters. One would miss punctuation chars when comparing it to the
        :py:func:`create_salt <arobito.Base.create_salt>` method.

        The test checks the correct length and the correct char output. It also checks if the correct errors are raised
        when one tries to create keys with a zero or negative length.
        """
        self.assertRaises(ValueError, arobito.Base.create_simple_key, 0)
        self.assertRaises(ValueError, arobito.Base.create_simple_key, -1)
        self.assertRaises(ValueError, arobito.Base.create_simple_key, -100)
        regex = re.compile('^[a-zA-Z0-9]+$', re.DOTALL)
        for i in range(1, 1000):
            salt = arobito.Base.create_simple_key(i)
            self.assertEqual(len(salt), i, 'Length of key is unexpected')
            self.failIf(regex.match(salt) is None, 'Key "{:s}" does not match the requirements'.format(salt))
        salt = arobito.Base.create_simple_key()
        # Checking the length is enough here - all other specifications are checked within the loop above.
        self.assertEqual(len(salt), 64, 'Key default length wrong')
