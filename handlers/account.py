#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import urllib

import tornado.web
import tornado.gen
import tornado.httpclient

from . import BaseHandler

class DoubanLoginHandler(BaseHandler):
    def get(self):
        self.redirect(r'https://www.douban.com/service/auth2/auth?client_id=%s&redirect_uri=%s&response_type=code&scope=book_basic_r,book_basic_w,douban_basic_common' %
                      (self.settings['api_key'], self.settings['callback']))

class CallbackHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        error = self.get_query_argument('error', None)
        code = self.get_query_argument('code', None)
        if error or not code:
            self.send_message('授权失败')
            self.redirect('/')
            return
        url = 'https://www.douban.com/service/auth2/token'
        data = {'client_id': self.settings['api_key'],
                'client_secret': self.settings['api_secret'],
                'redirect_uri': self.settings['callback'],
                'grant_type': 'authorization_code',
                'code': code}
        body = urllib.urlencode(data)
        http_client = tornado.httpclient.HTTPClient()
        response = http_client.fetch(url, method='POST', body=body)
        account_infor = json.loads(response.body)
        if not (yield self.async_db.members.find_one({'douban_user_id': account_infor['douban_user_id']})):
            yield self.async_db.members.insert({
                'douban_user_id': account_infor['douban_user_id'],
                'douban_user_name': account_infor['douban_user_name'],
                'access_token': account_infor['access_token'],
                'created': time.time()
            })
        else:
            yield self.async_db.members.update({'douban_user_id': account_infor['douban_user_id']}, {'$set': {'access_token': account_infor['access_token']}})
        self.set_secure_cookie('access_token', account_infor['access_token'], expires_days=7)
        self.redirect('/dashboard')

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')

handlers = [
    (r'/login', DoubanLoginHandler),
    (r'/login/callback', CallbackHandler),
    (r'/logout', LogoutHandler),
]