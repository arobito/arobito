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
This module contains the mapping between the CherryPy methods and the :py:mod:`ControllerBackend
<arobito.controlinterface.ControllerBackend>` module.
"""

import cherrypy
from arobito.controlinterface.ControllerBackend import App as Backend

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class App(object):
    """
    The Arobito Controlling Application
    """

    def __init__(self):
        """
        Initialize the backend
        """
        self.backend = Backend()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def auth(self) -> dict:
        """
        Answer to an authorization request.

        The request is a JSON post request that must look like this:

        .. code-block:: javascript

           {
             'username': 'The User Name',
             'password': 'The Password'
           }

        In case of a successful login, the response will look like this:

        .. code-block:: javascript

           {
             'auth':
             {
               'success': true,
               'status': 'Login successful',
               'key': 'The Session Key'
             }
           }

        Use the session key for all later requests.

        In case of a failed login, the default fail response will look like this:

        .. code-block:: javascript

           {
             'auth':
             {
               'success': false,
               'status': 'failed',
               'reason': 'User unknown or password wrong'
             }
           }

        This method returns a dict. The dict is automatically converted to JSON by CherryPy.

        This method refers to the backend method :py:meth:`ControllerBackend.App.auth <.ControllerBackend.App.auth>`.

        :return: The authorization response as a dict
        """
        return self.backend.auth(cherrypy.request.json)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def logout(self) -> dict:
        """
        Perform a logout with the given session key.

        A logout request must be a JSON post request that looks like the following:

        .. code-block:: javascript

           {
             'key': 'The Session Key'
           }

        A logout request gets always a positive response:

        .. code-block:: javascript

           {
             'logout': true
           }

        This method returns a dict that is converted to JSON by CherryPy.

        This method refers to the backend method :py:meth:`ControllerBackend.App.logout
        <.ControllerBackend.App.logout>`.

        :return: The positive response as a dict
        """
        return self.backend.logout(cherrypy.request.json)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def shutdown(self) -> dict:
        """
        Initiate the shutdown for the controlling application.

        This is only available to users of the level ``Administrator``. To initiate the shutdown, the following JSON
        needs to be posted:

        .. code-block:: javascript

           {
             'key': 'The Session Key'
           }

        The shutdown will be initiated within the next 10 seconds.

        In case of success, the response looks like the following:

        .. code-block:: javascript

           {
             'shutdown': true
           }

        The request fails on insufficient rights. The response is in this cases:

        .. code-block:: javascript

           {
             'shutdown': false
           }

        The dict that is returned by this method is converted to JSON by CherryPy.

        This method refers to the backend method :py:meth:`ControllerBackend.App.shutdown
        <.ControllerBackend.App.shutdown>`.

        :return: The response as dict
        """
        return self.backend.shutdown(cherrypy.request.json)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def get_session_count(self) -> dict:
        """
        Get the current session count.

        If the logged in user is an ``Administrator``, the count of currently active sessions is returned. The request
        must be a JSON post and looks like this:

        .. code-block:: javascript

           {
             'key': 'The Session Key'
           }

        In case of success, the number is returned (1 in this example):

        .. code-block:: javascript

           {
             'session_count': 1
           }

        If there are insufficient rights, -1 is returned as result:

        .. code-block:: javascript

           {
             'session_count': -1
           }

        The dict returned by this method is converted to JSON by CherryPy.

        This method refers to the backend method :py:meth:`ControllerBackend.App.get_session_count
        <.ControllerBackend.App.get_session_count>`.

        :return: The response as dict
        """
        return self.backend.get_session_count(cherrypy.request.json)
