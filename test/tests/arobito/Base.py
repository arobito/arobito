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

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class SingletonMock(object, metaclass=arobito.Base.SingletonMeta):
    """
    A mock class that is meant to be handled as a singleton.
    """

    def __init__(self):
        """
        Initialize class with a simple field
        """
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
    Test the singleton meta class (:py:class:`<arobito.Base.SingletonMeta>`)
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
    Test the :py:func:`<arobito.Base.create_salt>` function
    """

    def runTest(self) -> None:
        for i in range(1000):
            salt = arobito.Base.create_salt(i)
            self.assertEqual(len(salt), i, 'Length of salt is unexpected!')
            self.failIf('%' in salt, 'Salt contains a "%"')
        salt = arobito.Base.create_salt()
        self.assertEqual(len(salt), 128, 'Salt default length wrong')
