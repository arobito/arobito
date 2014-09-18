# -*- coding: utf-8 -*-

import os

__author__ = 'Juergen Edelbluth'


def get_config_folder():
    """
    Find a folder for the configuration files
    :return: The folder
    """
    folders = [os.environ.get('ROBI_CONF'), '/etc/robi', os.path.join(os.path.expanduser("~"), '.robi'), os.curdir]
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


def get_config_file(filename='robi.conf'):
    """
    Find the configuration file
    :type filename: str
    :return: str The path
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
