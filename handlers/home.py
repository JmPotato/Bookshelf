#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/dashboard')
        self.render('home.html')

class AboutHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/dashboard')
        self.render('about.html')

handlers = [
    (r'/', HomeHandler),
    (r'/about', AboutHandler),
]