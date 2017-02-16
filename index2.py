#!/usr/local/python/bin/python
#-*- coding: utf-8 -*-

from tornado.web import asynchronous, RequestHandler, Application, FallbackHandler
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado import ioloop
from optparse import OptionParser
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todolist.settings")
basedir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(basedir)

from django.core.wsgi import get_wsgi_application

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--port",
        dest="target",
        default=False,
        type="string",
        help="port")
    parser.add_option("-l", "--listen",
        dest="lsten",
        default=False,
        type="string",
        help="listen")

    (options, args) = parser.parse_args()

    if options.target:
        target = options.target
    else:
        exit(1)
    if options.lsten:
       listen = options.lsten
    else:
       listen = '127.0.0.1'
    wsgi_app = get_wsgi_application()
    tornado_app = Application([
            (r".*", FallbackHandler, dict(fallback=WSGIContainer(wsgi_app))),
        ])
    server = HTTPServer(tornado_app)
    server.listen(target, address=listen)
    ioloop.IOLoop.instance().start()
