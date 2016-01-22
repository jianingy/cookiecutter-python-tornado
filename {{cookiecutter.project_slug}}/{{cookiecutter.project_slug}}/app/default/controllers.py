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
from {{cookiecutter.project_slug}}.common.route import route
from {{cookiecutter.project_slug}}.common.controller import APIBaseController
from tornado.gen import coroutine


@route('/api/v1/version')
class VersionHandler(APIBaseController):

    def get(self):
        self.response(dict(version='{{cookiecutter.version}}'))


{%- if cookiecutter.use_database %}
@route('/api/v1/add/(\d+)/(\d+)')
class AddHandler(APIBaseController):

    @coroutine
    def get(self, x, y):
        from {{cookiecutter.project_slug}}.app.default.services import add
        retval = yield add(x, y)
        self.response(dict(x=x, y=y, val=retval))

{%- endif %}
