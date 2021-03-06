#!/usr/bin/env python3
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
This module is our primary test runner.

It iterates through all modules under the package test and searches for unit test test cases and runs them. This allows
adding tests simply by adding packages and classes. Only rule: All test case classes must reside in modules under the
``tests`` module.
"""

import os
import sys
from testlibs import Lister
import unittest

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


def test_suite_setup() -> None:
    """
    Setup the test runner: Make the Arobito source code accessible.
    """
    sys.path.insert(0, os.path.abspath('../src/'))


def run_tests() -> int:
    """
    Get all classes and run the tests.

    :return: 0 when all tests succeeded, 1 otherwise.
    """
    print('===================', file=sys.stderr)
    print('Arobito Test Runner', file=sys.stderr)
    print('===================', file=sys.stderr)
    print(file=sys.stderr)

    test_classes = Lister.enlist_all_classes('tests')

    run_count = 0
    failure_count = 0
    error_count = 0
    case_count = 0

    suite = unittest.TestSuite()

    for test_class in test_classes:
        __import__(test_class.__module__)
        if not issubclass(test_class, unittest.TestCase):
            continue
        case_count += 1
        suite.addTest(test_class())
        print('[{:>6d}] Test Case "{:s}.{:s}" enlisted.'
              .format(case_count, test_class.__module__, test_class.__name__), file=sys.stderr)

    print(file=sys.stderr)
    print('Running tests', file=sys.stderr)
    runner = unittest.TextTestRunner()
    module_result = runner.run(suite)
    run_count += module_result.testsRun
    failure_count += len(module_result.failures)
    error_count += len(module_result.errors)

    print(file=sys.stderr)
    print('---------------------------', file=sys.stderr)
    print('Arobito Test Runner Results', file=sys.stderr)
    print('---------------------------', file=sys.stderr)
    print('Tests enlisted: {:d}'.format(case_count), file=sys.stderr)
    print('Tests ran: {:d}'.format(run_count), file=sys.stderr)
    print('Failures: {:d}'.format(failure_count), file=sys.stderr)
    print('Errors: {:d}'.format(error_count), file=sys.stderr)

    print(file=sys.stderr)
    if error_count > 0 or failure_count > 0:
        print('TEST RUN FAILED.', file=sys.stderr)
        return 1

    print('TEST RUN SUCCESSFUL.', file=sys.stderr)
    return 0


if __name__ == '__main__':
    test_suite_setup()
    # Important: Return with the return code from the run!
    sys.exit(run_tests())