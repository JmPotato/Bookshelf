#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import tornado.web
import tornado.gen

from . import BaseHandler

class DashboardHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        member = self.get_member(self.get_current_user()['id'])
        self.render('dashboard/dashboard.html', member = member)
        print(self.get_current_user())

class ListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass

class StatisticsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass

handlers = [
    (r'/dashboard', DashboardHandler),
    (r'/dashboard/list', ListHandler),
    (r'/dashboard/statistics', StatisticsHandler),
]