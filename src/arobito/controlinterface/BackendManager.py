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
This module contains the base structure of the CherryPy based web interface. It configures CherryPy and mounts some
basic applications.

Additionally, it provides an User and a Session Manager to handle login requests, user privileges and associated
sessions.
"""


from arobito.Base import SingletonMeta, create_salt, hash_password, create_simple_key
from arobito import FsTools
import configparser
import re
import time

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class UserManager(object, metaclass=SingletonMeta):
    """
    This class manages the users. It is used to grant access.

    This is a singleton.
    """

    username_regex = re.compile('^[a-zA-Z0-9]{1,64}$')

    def __init__(self):
        """
        Load the user basic configuration from the users.ini file.

        :raise IOError: When there can be no users.ini can be loaded or created.
        """
        self.conf_file = FsTools.get_config_file('users.ini')
        config = configparser.ConfigParser()
        config.read(self.conf_file)
        config_changed = False
        if not '_Config_' in config.sections():
            config.add_section('_Config_')
            config.set('_Config_', 'secret', create_salt())
            config_changed = True
        if config_changed:
            with open(self.conf_file, 'w') as fh:
                config.write(fh)
                fh.flush()
                fh.close()
                config_changed = False
        if not 'secret' in config['_Config_']:
            config.set('_Config_', 'secret', create_salt())
            config_changed = True
        if config_changed:
            with open(self.conf_file, 'w') as fh:
                config.write(fh)
                fh.flush()
                fh.close()
                config_changed = False
        if len(config.sections()) < 1:
            raise IOError('Invalid configuration in "{:s}"'.format(self.conf_file))
        self.secret = config['_Config_']['secret']
        if len(config.sections()) == 1:
            # No std user!
            config.add_section('User:arobito')
            config.set('User:arobito', 'level', 'Administrator')
            salt = create_salt()
            config.set('User:arobito', 'salt', salt)
            config.set('User:arobito', 'password', hash_password('arobito', salt=salt, secret=self.secret))
            config.set('User:arobito', 'enabled', 'yes')
            config_changed = True
        if config_changed:
            with open(self.conf_file, 'w') as fh:
                config.write(fh)
                fh.flush()
                fh.close()
        self.config = config

    def get_user_by_username_and_password(self, username: str, password: str) -> dict:
        """
        Try to find a user and check the password. If a match is found, create a dict that contains the username, the
        userlevel, the timestamp of login and the timestamp of the last access.

        :param username: The username
        :param password: The password
        :return: The described dict or None on invalid credentials or inactive user account.
        """
        if username is None:
            return None
        if password is None:
            return None
        if not UserManager.username_regex.match(username):
            return None
        user_section = 'User:{:s}'.format(username)
        if not user_section in self.config.sections():
            return None
        section = self.config[user_section]
        level = 'level' in section and section['level'] or None
        salt = 'salt' in section and section['salt'] or None
        saved_password = 'password' in section and section['password'] or None
        enabled = 'enabled' in section and section['enabled'] or None
        if level is None or enabled is None:
            return None
        if enabled.lower() != 'yes':
            return None
        password_to_compare = hash_password(password, salt=salt, secret=self.secret)
        if password_to_compare != saved_password:
            return None
        return dict(username=username, level=level, timestamp=time.time(), last_access=time.time())


class SessionManager(object, metaclass=SingletonMeta):
    """
    This class, a singleton, manages the sessions.
    """

    def __init__(self):
        """
        Loads session defaults from the 'controller.ini' configuration file.
        """
        self.conf_file = FsTools.get_config_file('controller.ini')
        config = configparser.ConfigParser()
        config.read(self.conf_file)
        config_changed = False
        if not 'SessionManagement' in config.sections():
            config.add_section('SessionManagement')
            config.set('SessionManagement', 'max_age_seconds', '86400')
            config.set('SessionManagement', 'max_inactivity', '3600')
            config_changed = True
        if config_changed:
            with open(self.conf_file, 'w') as fh:
                config.write(fh)
                fh.flush()
                fh.close()
                config_changed = False
        if not 'max_age_seconds' in config['SessionManagement']:
            config.set('SessionManagement', 'max_age_seconds', '86400')
            config_changed = True
        if not 'max_inactivity' in config['SessionManagement']:
            config.set('SessionManagement', 'max_inactivity', '3600')
            config_changed = True
        if config_changed:
            with open(self.conf_file, 'w') as fh:
                config.write(fh)
                fh.flush()
                fh.close()
        self.config = config
        self.session_max_age = float(self.config['SessionManagement']['max_age_seconds'])
        self.session_max_inactivity = float(self.config['SessionManagement']['max_inactivity'])
        self.user_manager = UserManager()
        self.sessions = dict()

    def login(self, username: str, password: str) -> str:
        """
        Log a user in and create a session key on success.

        It calls the :py:meth:`cleanup() <.cleanup>` method first to throw old sessions away.

        :param username: The username
        :param password: The password
        :return: A session key or None on login failed
        """
        self.cleanup()
        user = self.user_manager.get_user_by_username_and_password(username, password)
        if user is None:
            return None
        key = create_simple_key()
        self.sessions[key] = user
        return key

    def logout(self, session: str) -> None:
        """
        Log a user out

        :param session: The session to log out
        """
        if not session is None:
            self.sessions.pop(session, None)

    def cleanup(self) -> None:
        """
        Clean left-over and old sessions from the SessionManager
        """
        current_time = time.time()
        for d in self.sessions:
            user = self.sessions.get(d, None)
            if user is None:
                continue
            age = current_time - user['timestamp']
            last_access = current_time - user['last_access']
            if age > self.session_max_age:
                self.logout(d)
                continue
            if last_access > self.session_max_inactivity:
                self.logout(d)

    def get_user(self, session: str) -> dict:
        """
        Get the user data dict by session ID

        It calls the :py:meth:`cleanup() <.cleanup>` method first to throw old sessions away.

        :param session: The session ID to look up
        :return: The dict or None if not there or already invalid.
        """
        self.cleanup()
        if session is None:
            return None
        if not session in self.sessions:
            return None
        self.sessions[session]['last_access'] = time.time()
        return self.sessions[session]

    def get_current_sessions(self) -> int:
        """
        Get the amount of active sessions.

        It calls the :py:meth:`cleanup() <.cleanup>` method first to throw old sessions away.

        :return: The count of active sessions.
        """
        self.cleanup()
        return len(self.sessions)
