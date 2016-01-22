# -*- coding: utf-8 -*-
#
# This piece of code is written by
#    {{cookiecutter.full_name}} <{{cookiecutter.email}}>
# with love and passion!
#
#        H A P P Y    H A C K I N G !
#              _____               ______
#     ____====  ]OO|_n_n__][.      |    |
#    [________]_|__|________)<     |YANG|
#     oo    oo  'oo OOOO-| oo\\_   ~o~~~o~
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                             21 Jan, 2016
#
import tornado.web
from json import dumps as json_encode


class BaseController(tornado.web.RequestHandler):
    pass


class APIBaseController(BaseController):

    def response(self, data):
        self.write(json_encode(data))
        self.finish()


class HTMLBaseController(BaseController):
    pass
