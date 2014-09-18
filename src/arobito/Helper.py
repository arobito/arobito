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
This module provides some basic helper functions needed globally.
"""

import cherrypy
import sys
from threading import Timer

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


def shutdown(code: int=0, delay: int=0) -> None:
    """
    Shutdown the CherryPy engine and exit the program.

    The shutdown can be delayed.

    :param code: Return code
    :param delay: Delay in seconds
    """
    if delay > 0:
        timer = Timer(float(delay), shutdown, kwargs={'code': code, 'delay': 0})
        timer.start()
        return
    cherrypy.engine.exit()
    sys.exit(code)
