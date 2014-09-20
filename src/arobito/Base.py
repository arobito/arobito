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
This module contains some very basic stuff needed all over the whole project. It is kind of a base library.
"""

import string
import random
import hashlib
from os.path import dirname
import sys

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class SingletonMeta(type):
    """
    Make a class a singleton.

    Add ``metaclass=SingletonMeta`` to the class' options to make it a singleton.
    """
    #: Store the instances in a private but static dictionary
    __instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


def create_salt(length: int=128) -> str:
    """
    Create a random string that works as a standard salt.

    It selects ``length`` chars form letters, digest and punctuation chars excluding the percent sign. By today, 128
    chars seems to be a sufficient salt length.

    :param length: Length of the random string
    :return: A random string
    """
    char_set = (string.ascii_letters + string.digits + string.punctuation).replace('%', '')
    return ''.join(random.sample(char_set * length, length))


def hash_password(password: str, salt: str, rounds: int=1000, secret: str=None) -> str:
    """
    Hash a given password

    The hash algorithm used is SHA-512. The hash is returned as a string of hex numbers ('a1b2c3d4e5f6aa...'). If a salt
    is defined, it is added to the password/the hash on each round of hashing. The secret is added only once. To make it
    harder to compromise, there are a lot of rounds of re-hashing hash+salt. 1000 rounds is the default.

    Attention: If you don't use a salt or zero rounds, the hashing is 100 percent useless. You might want to create a
    salt using the :py:func:`create_salt() <.create_salt>` function in this module.

    :param password: The clear text password
    :param salt: The salt (a random string)
    :param rounds: The number of rounds of hashing
    :param secret: The application secret
    :return: A string of hex numbers
    """
    h = hashlib.new('sha512')
    data = password
    if not secret is None:
        data += secret
    for i in range(1, rounds):
        if not salt is None:
            data += salt
        h.update(str.encode(data))
        data = h.hexdigest()
    return data


def create_simple_key(length: int=64) -> str:
    """
    Create a random key

    This key can be used for creating session IDs. The default length is 64 to prevent collisions.

    :param length: The length of the random string
    :return: A random string
    """
    char_set = (string.ascii_letters + string.digits)
    return ''.join(random.sample(char_set * length, length))


def find_root_path() -> str:
    """
    Find the application's root path in the file system

    :return: The root path as string
    """
    if hasattr(sys, "frozen"):
        return dirname(sys.executable)
    return sys.path[0]