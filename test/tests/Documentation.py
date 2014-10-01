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
The Documentation Module contains tests about the source code documentation.
"""

import unittest
from testlibs import Lister
import sys
from datetime import datetime

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class DefaultFields(unittest.TestCase):
    """
    This test case checks if every module has the required fields like

    - ``__license__``
    - ``__copyright__``
    - ``__author__``
    - ``__credits__``
    - ``__maintainer__``

    This ensures a minimum of documentation.
    """

    def __check_license(self, mod: str, fields: list) -> None:
        """
        Check if the __license__ field contains our standard text.

        :param mod: Name of the module to check
        :param fields: List of fields in the module
        """
        self.failIf('__license__' not in fields, '__license__ not set for module {:s}'.format(mod))
        self.assertEqual(sys.modules[mod].__license__, 'Apache License V2.0',
                         '__license__ wrong for module {:s}'.format(mod))

    def __check_copyright(self, mod: str, fields: list) -> None:
        """
        Check if the __copyright__ field contains our standard text.

        :param mod: Name of the module to check
        :param fields: List of fields in the module
        """
        self.failIf('__copyright__' not in fields,  '__copyright__ not set for module {:s}'.format(mod))
        self.assertEqual(sys.modules[mod].__copyright__,
                         'Copyright {:d} The Arobito Project'.format(datetime.now().year),
                         '__copyright__ wrong for module {:s}'.format(mod))

    def __check_author(self, mod: str, fields: list) -> None:
        """
        Check if the __author__ field is set up correctly.

        :param mod: Name of the module to check
        :param fields: List of fields in the module
        """
        self.failIf('__author__' not in fields, '__author__ not set for module {:s}'.format(mod))
        self.failIf(type(sys.modules[mod].__author__) is not str, ' Invalid __author__ type in module {:s}'.format(mod))
        self.failIf(len(sys.modules[mod].__author__.strip()) <= 0,  'No __author__ set in module {:s}'.format(mod))
        self.assertEqual(len(sys.modules[mod].__author__), len(sys.modules[mod].__author__.strip()),
                         '__author__ contains whitespaces at start or end {:s}'.format(mod))

    def __check_credits(self, mod: str, fields: list) -> None:
        """
        Check if the __credits__ field is set up correctly.

        :param mod: Name of the module to check
        :param fields: List of fields in the module
        """
        self.failIf('__credits__' not in fields, '__credits__ not set for module {:s}'.format(mod))
        self.failIf(type(sys.modules[mod].__credits__) is not list,
                    '__credits__ are not defined as list in module {:s}'.format(mod))
        self.failIf(len(sys.modules[mod].__credits__) <= 0, 'No __credits__ are provided in module {:s}'.format(mod))
        for a in sys.modules[mod].__credits__:
            self.failIf(type(a) is not str,
                        'At least one element in __credits__ is not a string in module {:s}'.format(mod))
            self.failIf(len(a.strip()) <= 0, 'At least one element in __credits__ is empty in module {:s}'.format(mod))
            self.assertEqual(len(a), len(a.strip()),
                             'At least one element in __credits__ contains whitespaces at start or end in module {:s}'
                             .format(mod))

    def __check_maintainer(self, mod: str, fields: list) -> None:
        """
        Check if the __maintainer__ field is set up correctly.

        :param mod: Name of the module to check
        :param fields: List of fields in the module
        """
        self.failIf('__maintainer__' not in fields, '__maintainer__ not set for module {:s}'.format(mod))
        self.failIf(type(sys.modules[mod].__maintainer__) is not str,
                    ' Invalid __maintainer__ type in module {:s}'.format(mod))
        self.failIf(len(sys.modules[mod].__maintainer__.strip()) <= 0,
                    'No __maintainer__ set in module {:s}'.format(mod))
        self.assertEqual(len(sys.modules[mod].__maintainer__), len(sys.modules[mod].__maintainer__.strip()),
                         '__maintainer__ contains whitespaces at start or end {:s}'.format(mod))

    def runTest(self) -> None:
        """
        Go though all modules and launch the tests for every single one.
        """
        candidates_arobito = Lister.enlist_all_modules()
        candidates_tests = Lister.enlist_all_modules('tests')
        candidates = candidates_arobito + candidates_tests
        for module_name in candidates:
            if '.' in module_name:
                pod = module_name.split('.')
                mod = __import__(module_name, globals(), locals(), pod[-1])
            else:
                mod = __import__(module_name, globals(), locals())
            fields = dir(mod)
            self.__check_license(module_name, fields)
            self.__check_copyright(module_name, fields)
            self.__check_author(module_name, fields)
            self.__check_credits(module_name, fields)
            self.__check_maintainer(module_name, fields)
