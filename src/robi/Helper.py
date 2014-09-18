# -*- coding: utf-8 -*-

import cherrypy
import sys
from threading import Timer

__author__ = 'Juergen Edelbluth'


def shutdown(code=0, delay=0):
    if delay > 0:
        timer = Timer(float(delay), shutdown, kwargs={'code': code, 'delay': 0})
        timer.start()
        return
    cherrypy.engine.exit()
    sys.exit(code)
