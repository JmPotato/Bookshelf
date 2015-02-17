#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path

import tornado.web
import tornado.ioloop
import tornado.httpserver

import urls
from init_db import db, async_db
from settings import *
from tornado.options import define, options

major = sys.version_info[0]
if major < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

define('port', default=8080, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            autoescape = None,
            google_analytics = google_analytics.lstrip(),
            cookie_secret = cookie_secret,
            api_key = api_key,
            api_secret = api_secret,
            callback = callback,
            xsrf_cookies = True,
            login_url = "/login",
            debug = Debug,
        )
        tornado.web.Application.__init__(self, urls.handlers, **settings)

        self.db = db
        self.async_db = async_db

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
