# -*- coding: utf-8 -*-

import cherrypy
from sys import stderr
from os import path
import re
from robi.controlinterface import Controller
import traceback
from robi.Base import SingletonMeta, find_root_path
from robi import FsTools
import configparser

__author__ = 'Juergen Edelbluth'


class RobiControlInterfaceStatics(object):

    mime_extract_regex = re.compile('\.(?P<attr>[^\.]+?)$', re.IGNORECASE)
    default_mime_type = 'application/octet-stream'
    mime_types = dict(html='application/xhtml+xml', png='image/png', gif='image/gif', jpeg='image/jpeg',
                      jpg='image/jpeg', css='text/css', js='text/javascript', xml='application/xml',
                      xhtml='application/xhtml+xml')

    """
    Serve static content out of the package
    """
    def __init__(self):
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
    def default(self, *args):
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
        match = RobiControlInterfaceStatics.mime_extract_regex.search(file)
        if not match:
            print('Statics Server: File does not match mime regex: "{:s}"'.format(file), file=stderr)
            raise cherrypy.HTTPError(404, 'File not found')
        mt = match.group('attr').lower()
        mime = RobiControlInterfaceStatics.mime_types.get(mt, RobiControlInterfaceStatics.default_mime_type)
        cherrypy.response.headers['Content-type'] = mime
        try:
            with open(file, 'rb') as fh:
                file_bytes = fh.read()
        except Exception as e:
            raise cherrypy.HTTPError(500, 'File read problem: ' + e.__str__())
        return file_bytes


class RobiControlInterfaceRedirect(object):
    """
    The control application itself
    """
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/static/index.html")


class RobiControlInterface(object, metaclass=SingletonMeta):
    """
    Main Class to control the Robi Web Based Interface
    """
    def __init__(self, bind_ip='0.0.0.0', listen_port=9812):
        """
        Configure a control server for Robi
        :param bind_ip: The IP to bind to
        :param listen_port: The port to listen to
        """
        self.bind_ip = bind_ip
        self.listen_port = listen_port
        pass

    def startup(self):
        """
        Start the Server
        :rtype : int
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
            cherrypy.tree.mount(RobiControlInterfaceRedirect(), '/', {'/': {
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
            cherrypy.tree.mount(RobiControlInterfaceStatics(), '/static', {'/': {
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
