#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from robi.controlinterface.ControlInterface import RobiControlInterface

__author__ = 'Juergen Edelbluth'


def control_interface(bind_ip='0.0.0.0', listen_port=9812):
    """
    Launches the Robi Control Interface
    :rtype : int
    :type bind_ip: str
    :type listen_port: int
    """
    rci = RobiControlInterface(bind_ip, listen_port)
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
