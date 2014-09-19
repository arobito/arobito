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
Parts of the web application
"""

import cherrypy
from sys import stderr
from os import path
import re
from arobito.controlinterface import Controller
import traceback
from arobito.Base import SingletonMeta, find_root_path
from arobito import FsTools
import configparser

__license__ = 'Apache License V2.0'
__copyright__ = 'Copyright 2014 The Arobito Project'
__author__ = 'Jürgen Edelbluth'
__credits__ = ['Jürgen Edelbluth']
__maintainer__ = 'Jürgen Edelbluth'


class ArobitoControlInterfaceStatics(object):
    """
    This class delivers static content over the web interface, e.g. JavaScript, HTML files, CSS files and images.
    """

    #: find the mime type by file ending
    mime_extract_regex = re.compile('\.(?P<attr>[^\.]+?)$', re.IGNORECASE)
    #: when no mime type could be identified
    default_mime_type = 'application/octet-stream'
    #: supported mime types by file ending
    mime_types = dict(html='application/xhtml+xml', png='image/png', gif='image/gif', jpeg='image/jpeg',
                      jpg='image/jpeg', css='text/css', js='text/javascript', xml='application/xml',
                      xhtml='application/xhtml+xml')

    def __init__(self):
        """
        Look in the config file 'controller.ini' for the folder with the static contents to serve.
        """
        self.conf_file = FsTools.get_config_file('controller.ini')
        config = configparser.ConfigParser()
        config.read(self.conf_file)
        config_changed = False
        if not 'Server' in config.sections():
            config.add_section('Server')
            config.set('Server', 'static-folder', path.join(find_root_path(), 'web-static'))
            config_changed = True
        if config_changed:
            with open(self.conf_file, 'w') as fh:
                config.write(fh)
                fh.flush()
                fh.close()
                config_changed = False
        if not 'static-folder' in config['Server']:
            config.set('Server', 'static-folder', path.join(find_root_path(), 'web-static'))
            config_changed = True
        if config_changed:
            with open(self.conf_file, 'w') as fh:
                config.write(fh)
                fh.flush()
                fh.close()
                config_changed = True
        static_folder = config.get('Server', 'static-folder')
        if static_folder is None or len(static_folder) <= 0:
            config.set('Server', 'static-folder', path.join(find_root_path(), 'web-static'))
            config_changed = True
        if config_changed:
            with open(self.conf_file, 'w') as fh:
                config.write(fh)
                fh.flush()
                fh.close()
        static_folder = config.get('Server', 'static-folder')
        self.root_dir = static_folder

    @cherrypy.expose
    def default(self, *args) -> bytes:
        """
        Serve static content directly out of the package
        """
        if len(args) <= 0:
            raise cherrypy.HTTPError(404, 'File not found')
        file = self.root_dir
        for a in args:
            if a is None:
                print('Statics Server: Invalid part: It is "None"', file=stderr)
                raise cherrypy.HTTPError(404, 'File not found')
            if not type(a) == str:
                print('Statics Server: Invalid part: Is not a string', file=stderr)
                raise cherrypy.HTTPError(404, 'File not found')
            a = str(a)
            if a.startswith('..'):
                print('Statics Server: Invalid part: "{:s}" starts with ".."'.format(a), file=stderr)
                raise cherrypy.HTTPError(404, 'File not found')
            file = path.join(file, a)
        if not path.exists(file):
            print('Statics Server: File does not exist: "{:s}"'.format(file), file=stderr)
            raise cherrypy.HTTPError(404, 'File not found')
        if not path.isfile(file):
            print('Statics Server: File is not a file: "{:s}"'.format(file), file=stderr)
            raise cherrypy.HTTPError(404, 'File not found')
        match = ArobitoControlInterfaceStatics.mime_extract_regex.search(file)
        if not match:
            print('Statics Server: File does not match mime regex: "{:s}"'.format(file), file=stderr)
            raise cherrypy.HTTPError(404, 'File not found')
        mt = match.group('attr').lower()
        mime = ArobitoControlInterfaceStatics.mime_types.get(mt, ArobitoControlInterfaceStatics.default_mime_type)
        cherrypy.response.headers['Content-type'] = mime
        try:
            with open(file, 'rb') as fh:
                file_bytes = fh.read()
        except Exception as e:
            raise cherrypy.HTTPError(500, 'File read problem: ' + e.__str__())
        return file_bytes


class ArobitoControlInterfaceRedirect(object):
    """
    On the web interface root, make a simple redirect to the static index page.
    """
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/static/index.html")


class ArobitoControlInterface(object, metaclass=SingletonMeta):
    """
    Main Class to control the Robi Web Based Interface
    """
    def __init__(self, bind_ip: str='0.0.0.0', listen_port: int=9812):
        """
        Configure a control server for Robi
        :param bind_ip: The IP to bind to
        :param listen_port: The port to listen to
        """
        self.bind_ip = bind_ip
        self.listen_port = listen_port
        pass

    def startup(self) -> int:
        """
        Start the Server

        :returns: The exit status code
        """
        cherrypy.log.access_file = None
        cherrypy.log.screen = None

        csp = "default-src 'none'; " \
              "script-src 'self' 'unsafe-inline'; " \
              "style-src 'self' 'unsafe-inline'; " \
              "img-src 'self' data:; " \
              "connect-src 'self'; " \
              "font-src 'none'; " \
              "object-src 'none'; " \
              "media-src 'none'; " \
              "frame-src 'none'"
        try:
            cherrypy.config.update({'global': {
                'server.socket_host': self.bind_ip,
                'server.socket_port': self.listen_port,
                'autoreload.on': False
            }})
            cherrypy.tree.mount(ArobitoControlInterfaceRedirect(), '/', {'/': {
                'tools.gzip.on': False,
                'tools.encode.on': False,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [
                    ('X-Frame-Options', 'DENY'),
                    ('X-XSS-Protection', '1; mode=block'),
                    ('Content-Security-Policy', csp),
                    ('X-Content-Security-Policy', csp),
                    ('X-Webkit-CSP', csp),
                    ('X-Content-Type-Options', 'nosniff')
                ]
            }})
            cherrypy.tree.mount(ArobitoControlInterfaceStatics(), '/static', {'/': {
                'tools.gzip.on': False,
                'tools.encode.on': False,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [
                    ('X-Frame-Options', 'DENY'),
                    ('X-XSS-Protection', '1; mode=block'),
                    ('Content-Security-Policy', csp),
                    ('X-Content-Security-Policy', csp),
                    ('X-Webkit-CSP', csp),
                    ('X-Content-Type-Options', 'nosniff')
                ]
            }})
            cherrypy.tree.mount(Controller.App(), '/app', {'/': {
                'tools.gzip.on': False,
                'tools.encode.on': False,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [
                    ('X-Frame-Options', 'DENY'),
                    ('X-XSS-Protection', '1; mode=block'),
                    ('Content-Security-Policy', csp),
                    ('X-Content-Security-Policy', csp),
                    ('X-Webkit-CSP', csp),
                    ('X-Content-Type-Options', 'nosniff')
                ]
            }})
            cherrypy.engine.start()
            cherrypy.engine.block()
            return 0
        except Exception as e:
            print('Cannot start internal service: {:s}:\n{:s}'.format(e.__str__(), traceback.format_exc()), file=stderr)
            return -1
