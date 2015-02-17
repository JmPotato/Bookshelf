#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json

import tornado.web
import tornado.escape
import tornado.httpclient
from bson.objectid import ObjectId

os.environ['TZ'] = 'Asia/Shanghai'
time.tzset()

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def async_db(self):
        return self.application.async_db

    @property
    def messages(self):
        if not hasattr(self, '_messages'):
            messages = self.get_secure_cookie('saved_message')
            self._messages = []
            if messages:
                self._messages = tornado.escape.json_decode(messages)
        return self._messages

    def send_message(self, message, type = 'danger'):
        self.messages.append((type, message))
        self.set_secure_cookie('saved_message',
                               tornado.escape.json_encode(self.messages))

    def get_message(self):
        messages = self.messages
        self._messages = []
        self.clear_cookie('saved_message')
        return messages

    def format_time(self, t):
        now = time.time()
        diff = abs(now - t)
        if diff < 60:
            utc = '%d 秒前' % (diff if diff > 1 else 1)
        elif diff < 3600:
            utc = '%d 分钟前' % (diff / 60)
        elif diff < 3600 * 24:
            utc = '%d 小时前' % (diff / 3600)
        elif diff <= 3600 * 24 * 7:
            utc = '%d 天前' % (diff / 3600 / 24)
        else:
            now = time.localtime(now)
            t = time.localtime(t)
            if t.tm_year == now.tm_year:
                utc = time.strftime('%m-%d %H:%M:%S', t)
            else:
                utc = time.strftime('%Y-%m-%d %H:%M:%S', t)
        return utc

    def get_current_user(self):
        access_token = self.get_secure_cookie('access_token')
        if not access_token:
            return
        url = 'https://api.douban.com/v2/user/~me'
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        http_client = tornado.httpclient.HTTPClient()
        response = http_client.fetch(url, method='GET', headers=headers)
        http_client.close()
        return json.loads(response.body)

    def get_member(self, douban_user_id):
        member = self.db.members.find_one({'douban_user_id': douban_user_id})
        if not member:
            raise tornado.web.HTTPError(404)
        return member
