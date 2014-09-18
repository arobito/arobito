# -*- coding: utf-8 -*-

import string
import random
import hashlib
from os.path import dirname
import sys

__author__ = 'Juergen Edelbluth'


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def create_salt(length=128):
    char_set = (string.ascii_letters + string.digits + string.punctuation).replace('%', '')
    return ''.join(random.sample(char_set * length, length))


def hash_password(password, salt=None, rounds=1000, secret=None):
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


def create_simple_key(length=32):
    char_set = (string.ascii_letters + string.digits)
    return ''.join(random.sample(char_set * length, length))


def find_root_path():
    if hasattr(sys, "frozen"):
        return dirname(sys.executable)
    return sys.path[0]