# -*- coding: utf-8 -*-

import cherrypy
from robi.Base import SingletonMeta, create_salt, hash_password, create_simple_key
from robi import FsTools
import configparser
import re
import time
from robi import Helper

__author__ = 'Juergen Edelbluth'


class UserManager(object, metaclass=SingletonMeta):
    """
    Use this to handle user logins
    """

    username_regex = re.compile('^[a-zA-Z0-9]{1,64}$')

    def __init__(self):
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
            config.add_section('User:robi')
            config.set('User:robi', 'level', 'Administrator')
            salt = create_salt()
            config.set('User:robi', 'salt', salt)
            config.set('User:robi', 'password', hash_password('robi', salt=salt, secret=self.secret))
            config.set('User:robi', 'enabled', 'yes')
            config_changed = True
        if config_changed:
            with open(self.conf_file, 'w') as fh:
                config.write(fh)
                fh.flush()
                fh.close()
        self.config = config

    def get_user_by_username_and_password(self, username, password):
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
    Provide a session management for the controller
    """
    def __init__(self):
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

    def login(self, username, password):
        self.cleanup()
        user = self.user_manager.get_user_by_username_and_password(username, password)
        if user is None:
            return None
        key = create_simple_key()
        self.sessions[key] = user
        return key

    def logout(self, session):
        self.cleanup()
        if not session is None:
            self.sessions.pop(session, None)

    def cleanup(self):
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

    def get_user(self, session):
        self.cleanup()
        if session is None:
            return None
        if not session in self.sessions:
            return None
        self.sessions[session]['last_access'] = time.time()
        return self.sessions[session]

    def get_current_sessions(self):
        self.cleanup()
        return len(self.sessions)


class App(object):
    """
    The main Application
    """
    auth_default_response = dict(auth=dict(success=False, status='failed', reason='User unknown or password wrong'))

    def __init__(self):
        self.locked = True
        try:
            self.session_manager = SessionManager()
            self.locked = False
        except IOError:
            pass

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def auth(self):
        if self.locked:
            return App.auth_default_response
        json = cherrypy.request.json
        username = None
        password = None
        if 'username' in json:
            username = json['username']
        if 'password' in json:
            password = json['password']
        if username is None or password is None:
            return App.auth_default_response
        key = self.session_manager.login(username, password)
        if key is None:
            return App.auth_default_response
        return dict(auth=dict(success=True, status='Login successful', key=key))

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def logout(self):
        json = cherrypy.request.json
        if 'key' in json:
            self.session_manager.logout(json['key'])
        return dict(logout=True)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def shutdown(self):
        json = cherrypy.request.json
        if not 'key' in json:
            return dict(shutdown=False)
        user = self.session_manager.get_user(json['key'])
        if user is None:
            return dict(shutdown=False)
        if user['level'] == 'Administrator':
            Helper.shutdown(delay=10)
            return dict(shutdown=True)
        else:
            return dict(shutdown=False)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def get_session_count(self):
        json = cherrypy.request.json
        if not 'key' in json:
            return dict(session_count=-1)
        user = self.session_manager.get_user(json['key'])
        if user is None:
            return dict(session_count=-1)
        if user['level'] == 'Administrator':
            Helper.shutdown(delay=10)
            return dict(shutdown=self.session_manager.get_current_sessions())
        else:
            return dict(session_count=-1)
