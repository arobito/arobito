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
This module contains functionality to work with the local file system.

We need those functions to use configuration files and find out about their location.
"""

import os

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


def get_config_folder() -> str:
    """
    Find a folder for the configuration files

    The function first tries

    - to find the environment variable ``AROBITO_CONF``.
    - /etc/arobito
    - ~/.arobito
    - the current directory

    :return: The folder
    :raises: IOError when no location is sufficient.
    """
    folders = [
        os.environ.get('AROBITO_CONF'),
        '/etc/arobito',
        os.path.join(os.path.expanduser("~"), '.arobito'),
        os.curdir
    ]
    the_dir = None
    for loc in folders:
        if loc is None:
            continue
        if not os.path.exists(loc):
            continue
        if not os.path.isdir(loc):
            continue
        the_dir = loc
    if the_dir is None:
        raise IOError('Cannot determine config folder')
    return the_dir


def get_config_file(filename: str='arobito.conf') -> str:
    """
    Find the location of a configuration file

    :param filename: The name of the file to find
    :return: The location of the file
    :raises: IOError when no file can be found and created
    """
    config_folder = get_config_folder()
    config_file = os.path.join(config_folder, filename)
    if not os.path.exists(config_file):
        open(config_file, 'a').close()
    if not os.path.exists(config_file):
        raise IOError('Unable to find or create config file!')
    if not os.path.isfile(config_file):
        raise IOError('Requested file is not a file!')
    return config_file
