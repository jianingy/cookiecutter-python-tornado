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
from tornado.escape import json_encode, json_decode
from tornado.options import options as tornado_options
from traceback import format_exception
import tornado.web


class BaseController(tornado.web.RequestHandler):

    def fail(self, error_code, title, description=''):
        error = dict(error_code=error_code,
                     title=title, description=description)
        raise tornado.web.HTTPError(error_code / 1000, None, error)


class APIBaseController(BaseController):

    def __init__(self, *args, **kwargs):
        super(APIBaseController, self).__init__(*args, **kwargs)
        self.data = dict()

    def prepare(self):
        content_type = self.request.headers.get('Content-Type')

        if not self.request.body:
            return

        if not content_type:
            return

        if content_type.strip().lower().startswith('application/json'):
            try:
                self.data = json_decode(self.request.body)
            except:
                self.fail(400001, title='Invalid JSON data')

    def reply(self, data):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish(json_encode(data))

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            exc_type, exc, trace = kwargs['exc_info']
            if exc.args and isinstance(exc.args[0], dict):
                error = exc.args[0]
            else:
                error = dict()
            if tornado_options.debug:
                error['traceback'] = format_exception(exc_type, exc, trace)
            self.reply(error)


class HTMLBaseController(BaseController):

    def reply(self, name, data):
        self.set_header('Content-Type', 'text/html; charset=UTF-8')
        self.render('%s.html' % name, **data)

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            exc_type, exc, trace = kwargs['exc_info']
            if exc.args and isinstance(exc.args[0], dict):
                error = exc.args[0]
            else:
                error = dict()
            if tornado_options.debug:
                error['traceback'] = format_exception(exc_type, exc, trace)
            self.reply('error', error)
