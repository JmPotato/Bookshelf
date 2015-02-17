#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handlers import home, account, dashboard

handlers = []
handlers.extend(home.handlers)
handlers.extend(account.handlers)
handlers.extend(dashboard.handlers)