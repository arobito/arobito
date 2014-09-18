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
This is the main startup module for the Arobito Control Panel.

The panel itself is in charge of starting all other required services, like the connection to the micro controllers.

It all starts below the ``if __name__ == '__main__':`` line: First, parse all arguments and then activate the web based
control interface on a CherryPy foundation.
"""

import sys
import argparse
from arobito.controlinterface.ControlInterface import ArobitoControlInterface

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


def control_interface(bind_ip: str='0.0.0.0', listen_port: int=9812) -> int:
    """
    Launch the Arobito Control Interface - a web based remote control solution

    :param bind_ip: IP address to bind the control interface to. Use '0.0.0.0' for all available IP addresses.
    :param listen_port: The port number for the control interface to listen. Default is 9812.
    :return: A return code. 0 means 'everything is ok'
    """
    rci = ArobitoControlInterface(bind_ip, listen_port)
    return rci.startup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--bindip',
                        help='Specify the IP address to bind to (Default: 0.0.0.0)',
                        type=str, default='0.0.0.0')
    parser.add_argument('-p', '--listenport',
                        help='Specify the port to listen to (Default: 9812)',
                        type=int, default=9812)
    args = parser.parse_args()
    sys.exit(control_interface(bind_ip=args.bindip, listen_port=args.listenport))
