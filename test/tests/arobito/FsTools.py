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
import arobito.FsTools
import os

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class GetConfigFolder(unittest.TestCase):
    """
    Test the :py:func:`get_config_folder <arobito.FsTools.get_config_folder>` function

    For this test, it is very important, that there are no env variables are set and no special folders are created.
    """

    def __check_default(self):
        """
        Check the default folder returned, without additional configuration. It expects the current folder.
        """
        path_generated = os.path.abspath(arobito.FsTools.get_config_folder())
        path_expected = os.path.abspath(os.path.join(os.path.abspath(os.getcwd())))
        self.assertEqual(path_expected, path_generated, 'Path is not the one expected')

    def runTest(self):
        """
        This very basic test checks if the folder returned for the configuration files.
        """
        self.__check_default()