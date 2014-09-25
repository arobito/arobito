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


class SingletonMock1(object, metaclass=arobito.Base.SingletonMeta):
    """
    A mock class that is meant to be handled as a singleton. It is used by the :py:class:`Singleton <.Singleton>` test
    case.
    """

    def __init__(self):
        self.__value = 'After Init'

    def set_value(self, value: str) -> None:
        """
        Set the value

        :param value: The value
        """
        self.__value = value

    def get_value(self) -> str:
        """
        Get the value

        :return: The value
        """
        return self.__value


class SingletonMock2(object, metaclass=arobito.Base.SingletonMeta):
    """
    A mock class that is meant to be handled as a singleton. It is used by the :py:class:`Singleton <.Singleton>` test
    case. This is roughly the same thing as :py:class:`SingletonMock1 <.SingletonMock1>`, but it should be another
    Singleton instance.
    """

    def __init__(self):
        self.__value = 'After Init'

    def set_value(self, value: str) -> None:
        """
        Set the value

        :param value: The value
        """
        self.__value = value

    def get_value(self) -> str:
        """
        Get the value
        
        :return: The value
        """
        return self.__value


class Singleton(unittest.TestCase):
    """
    Test the singleton meta class (:py:class:`SingletonMeta <arobito.Base.SingletonMeta>`)

    Many things within this project rely on a working singleton implementation. It's very important that this behaviour
    is checked in every test run, especially when the language (Python) version changes.
    """

    def runTest(self) -> None:
        """
        Try to create two instances of the singleton (the test uses the :py:class:`SingletonMock1 <.SingletonMock1>`
        class) and tests if values and instances are equal.
        """
        test_string = 'Value set from test'
        singleton_one = SingletonMock1()
        singleton_one.set_value(test_string)
        singleton_two = SingletonMock1()
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


class DifferentSingletons(unittest.TestCase):
    """
    Find out if two different singletons are really independent
    """

    def runTest(self):
        """
        Try to create two different singletons and check if their value is different, getting and setting works on
        different objects and if the objects are different.
        """
        test_string = 'Value set from test'
        singleton_one = SingletonMock1()
        singleton_one.set_value(test_string)
        singleton_two = SingletonMock2()
        self.assertNotEqual(singleton_two.get_value(), test_string, 'Singleton 2 value equals the test string')
        self.assertNotEqual(singleton_one, singleton_two, 'Singleton 1 and 2 are equal')
        self.assertNotEqual(singleton_one.get_value(), singleton_two.get_value(),
                            'The values in Singleton 1 and Singleton 2 are +equal')
        test_string = 'Another value'
        singleton_two.set_value(test_string)
        self.assertNotEqual(singleton_one.get_value(), test_string, 'Singleton 1 value does match test string')
        self.assertNotEqual(singleton_one, singleton_two, 'Singleton 1 and 2 are equal')
        self.assertNotEqual(singleton_one.get_value(), singleton_two.get_value(),
                            'The values in Singleton 1 and Singleton 2 are equal')


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
        for i in range(1, 1000):
            salt = arobito.Base.create_salt(i)
            self.assertEqual(len(salt), i, 'Length of salt is unexpected')
            self.assertRegex(salt, '^[a-zA-Z0-9\|\^\.,;_\-:<>+\]\[\(\)\$!&=\"\'´`\*@:~\{\}#\?/\\\]+$',
                             'Salt "{:s}" does not match the requirements'.format(salt))
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
        for i in range(1, 1000):
            key = arobito.Base.create_simple_key(i)
            self.assertEqual(len(key), i, 'Length of key is unexpected')
            self.assertRegex(key, '^[a-zA-Z0-9]+$', 'Key "{:s}" does not match the requirements'.format(key))
        key = arobito.Base.create_simple_key()
        # Checking the length is enough here - all other specifications are checked within the loop above.
        self.assertEqual(len(key), 64, 'Key default length wrong')


class HashPassword(unittest.TestCase):
    """
    Test the :py:func:`hash_password <arobito.Base.hash_password>` function
    """

    def runTest(self) -> None:
        """
        Test if the method behaves correctly when fed with illegal parameters. Then it checks if the return value looks
        like a hash. And last but not least try some hashes that have been built with the ``sha512sum`` command on a
        Linux machine.
        """
        bad_password_values = [None, '']
        bad_round_values = [0, -1, -100, -1000]
        for x in bad_password_values:
            self.assertRaises(ValueError, arobito.Base.hash_password, password=x)
        for p in bad_password_values:
            for r in bad_round_values:
                self.assertRaises(ValueError, arobito.Base.hash_password, password=p, rounds=r)

        test_password = 'test1234'
        for salt in [None, 'aaa', '', arobito.Base.create_salt()]:
            for secret in [None, 'aaa', '', arobito.Base.create_salt()]:
                for rounds in range(1, 10000, 250):
                    self.assertRegex(arobito.Base.hash_password(test_password, salt, rounds, secret),
                                     '^[a-f0-9]{128}$', 'Hash does not match pattern')

        self.assertEqual(arobito.Base.hash_password(test_password, rounds=1),
                         '2bbe0c48b91a7d1b8a6753a8b9cbe1db16b84379f3f91fe115621284df7a48f1cd71e9beb90ea614c7bd924250a'
                         'a9e446a866725e685a65df5d139a5cd180dc9', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, rounds=2),
                         'f104fc22ae19d7fcaa8b0e66c9721d54fe108a771e0e06f075faa31ff4807032ed726127f214dfff12c48e4465e'
                         '4bc8d966b2924c8e58d9fd205c09cf81dcd46', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(
            password='2bbe0c48b91a7d1b8a6753a8b9cbe1db16b84379f3f91fe115621284df7a48f1cd71e9beb90ea614c7bd924250aa9e4'
                     '46a866725e685a65df5d139a5cd180dc9', rounds=1),
            'f104fc22ae19d7fcaa8b0e66c9721d54fe108a771e0e06f075faa31ff4807032ed726127f214dfff12c48e4465e4bc8d966b2924'
            'c8e58d9fd205c09cf81dcd46', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(
            password='f104fc22ae19d7fcaa8b0e66c9721d54fe108a771e0e06f075faa31ff4807032ed726127f214dfff12c48e4465e4bc8'
                     'd966b2924c8e58d9fd205c09cf81dcd46', rounds=1),
            'e741ee1b448a807965e130fccc92c1025a7eac670c33f137edd3da05f4d5a6eb4a3b35424c6a519a7029c1fe714fab383added36'
            '815b32f5962982a5c3d49be0', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, rounds=3),
                         'e741ee1b448a807965e130fccc92c1025a7eac670c33f137edd3da05f4d5a6eb4a3b35424c6a519a7029c1fe714'
                         'fab383added36815b32f5962982a5c3d49be0', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, secret='geek', rounds=1),
                         '438b36f99d6568d5195c377b3ef4e084acb9599620cc59f270f6b88b95557bcd83067a6901ed7c27aa47d6f17ee'
                         'ecdd5c807b965633930e8d0d6a0007f7a7e95', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, secret='geek', rounds=2),
                         '2d390befcdc2b4ade3dd607145cfe9c56c0ef5a0785f38f81d6818975365f8cb335d940720aa37961e3942bda56'
                         'b305158ddf30789b7e86893f3770f2391d3a5', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, secret='geek', rounds=3),
                         '6d773d1000bf10545b4a2bffd4ebf7921986380ed6c141573d1f7154a4fb636677e8935cd7bf30d9f179a848b87'
                         '1c4d6817c1542b38d76f09b9603389e977981', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, salt='geek', rounds=1),
                         '438b36f99d6568d5195c377b3ef4e084acb9599620cc59f270f6b88b95557bcd83067a6901ed7c27aa47d6f17ee'
                         'ecdd5c807b965633930e8d0d6a0007f7a7e95', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, salt='geek', rounds=2),
                         'af387d7860ed5c5ec5141f09dce42c9536bc4b008b4d1050849ff86c2ceea9052cfb7bd22367082226fbcd09f78'
                         '4491e0fa8e9ce259abe31c54994d22fac1e06', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, salt='geek', rounds=3),
                         '29fb7d24fdbd38d44e6747fa952d210826a625ae94c0f0a50d7fc9411ca7388030b261bfb98f08ad321a2ff73ab'
                         '896082b4acb0472e32463aa22a0b27394b6d3', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, salt='geek', secret='nerd', rounds=1),
                         '64b62fbd23556efcb4d078143f85629f3053bb130c43cc840c7d4b30d8b2cdd63a5a0224d6c9e69f048371300c3'
                         'e2ffcde8ef443c4c014c67b93349d3431384d', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, salt='geek', secret='nerd', rounds=2),
                         '9fc4437aae7243e3d251875d156986ced0c6d9171a9fd2bd6c2e8993d96aba910a986e700e3967a72c372831b31'
                         '729e6df16c2f1ec42e308af4fcdae11399e2d', 'Hash wrong')
        self.assertEqual(arobito.Base.hash_password(test_password, salt='geek', secret='nerd', rounds=3),
                         'e927a8cba9dfd49a7b6df2b5fffcc3d27317a22df4ab61b2c36b8b1c106f51a8d92337b60f792aa985dd9c011d1'
                         'd4d046de95ca38d03dc77595c7c1829fa1899', 'Hash wrong')
