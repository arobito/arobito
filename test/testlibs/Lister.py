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
This is the place to put functions that we need in many tests.
"""

from pkgutil import iter_modules as get_modules
import inspect
import sys

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


def _enlist_all_modules(list_of_modules: list, package: str='arobito') -> None:
    """
    List all modules within a given package and all subpackages.

    :param list_of_modules: A list that is filled with the modules found
    :param package: The name of the package
    """

    # Import the package
    if '.' in package:
        pod = package.split('.')
        pack = __import__(package, globals(), locals(), pod[-1])
    else:
        pack = __import__(package, globals(), locals())
    # Walk it
    for importer, mod_name, is_package in get_modules(pack.__path__, pack.__name__ + '.'):
        if is_package:
            _enlist_all_modules(list_of_modules=list_of_modules, package=mod_name)
            continue
        list_of_modules.append(mod_name)


def enlist_all_modules(package: str='arobito') -> list:
    """
    Return a list of all modules of the given package and all sub packages.

    :param package: The package name
    :return: The list of modules
    """
    list_of_modules = list()
    _enlist_all_modules(list_of_modules, package)
    return list_of_modules


def enlist_all_classes(package: str='arobito') -> list:
    """
    List all classes in the given package and all sub packages.

    :param package: The package name
    :return: List of all classes
    """
    # Get all the modules
    list_of_modules = enlist_all_modules(package)
    list_of_classes = list()
    # Get the classes
    for mod_name in list_of_modules:
        __import__(mod_name)
        class_members = inspect.getmembers(sys.modules[mod_name], inspect.isclass)
        for class_name, class_object in class_members:
                list_of_classes.append(class_object)

    return list_of_classes
