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
This module implements the methods for the main controller app. By decoupling them from the CherryPy exposed methods,
they are better to test without a mock.
"""

from arobito import Helper
from arobito.controlinterface.BackendManager import SessionManager

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class App(object):
    """
    This is the backend class for :py:class:`ControllerFrontend.App <arobito.controlinterface.ControllerFrontend.App>`.
    """

    #: The default response when authorization fails.
    auth_default_response = dict(auth=dict(success=False, status='failed', reason='User unknown or password wrong'))

    def __init__(self):
        """
        Initialize the main App with the :py:class:`SessionManager
        <arobito.controlinterface.BackendManager.SessionManager>` instance.
        """

        self.locked = True
        try:
            self.session_manager = SessionManager()
            self.locked = False
        except IOError:
            pass

    def auth(self, json_req: dict) -> dict:
        """
        Backend method for :py:meth:`ControllerFrontend.App.auth <.ControllerFrontend.App.auth>`

        :param json_req: The JSON request dict
        :return: Response as dictionary
        """

        if self.locked:
            return App.auth_default_response
        username = None
        password = None
        if 'username' in json_req:
            username = json_req['username']
        if 'password' in json_req:
            password = json_req['password']
        if username is None or password is None:
            return App.auth_default_response
        key = self.session_manager.login(username, password)
        if key is None:
            return App.auth_default_response
        return dict(auth=dict(success=True, status='Login successful', key=key))

    def logout(self, json_req: dict) -> dict:
        """
        Backend method for :py:meth:`ControllerFrontend.App.logout <.ControllerFrontend.App.logout>`

        :param json_req: The JSON request dict
        :return: Response as dictionary
        """

        if 'key' in json_req:
            self.session_manager.logout(json_req['key'])
        return dict(logout=True)

    def shutdown(self, json_req: dict) -> dict:
        """
        Backend method for :py:meth:`ControllerFrontend.App.shutdown <.ControllerFrontend.App.shutdown>`

        :param json_req: The JSON request dict
        :return: Response as dictionary
        """

        if not 'key' in json_req:
            return dict(shutdown=False)
        user = self.session_manager.get_user(json_req['key'])
        if user is None:
            return dict(shutdown=False)
        if user['level'] == 'Administrator':
            Helper.shutdown(delay=10)
            return dict(shutdown=True)
        else:
            return dict(shutdown=False)

    def get_session_count(self, json_req: dict) -> dict:
        """
        Backend method for :py:meth:`ControllerFrontend.App.get_session_count
        <.ControllerFrontend.App.get_session_count>`

        :param json_req: The JSON request dict
        :return: Response as dictionary
        """

        if not 'key' in json_req:
            return dict(session_count=-1)
        user = self.session_manager.get_user(json_req['key'])
        if user is None:
            return dict(session_count=-1)
        if user['level'] == 'Administrator':
            return dict(session_count=self.session_manager.get_current_sessions())
        else:
            return dict(session_count=-1)
