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
from {{ cookiecutter.project_slug }}.common.route import route
from {{ cookiecutter.project_slug }}.common import controller
from tornado.gen import coroutine
import pkg_resources


@route('/')
class IndexController(controller.HTMLBaseController):

    @coroutine
    def get(self):
        version = pkg_resources.require('{{ cookiecutter.project_slug }}')[0].version
        self.response('default/default',
                      dict(version=version))


@route('/api/v1/version')
class VersionController(controller.APIBaseController):

    @coroutine
    def get(self):
        version = pkg_resources.require('{{ cookiecutter.project_slug }}')[0].version
        self.response(dict(version=version))

{% if cookiecutter.use_database == 'y' %}
@route('/api/v1/add/(\d+)/(\d+)')
class AddController(controller.APIBaseController):

    @coroutine
    def get(self, x, y):
        from {{cookiecutter.project_slug}}.apps.default.services import add
        retval = yield add(x, y)
        self.response(dict(x=x, y=y, val=retval))
{% endif %}

@route('/api/v1/mul')
class MulController(controller.APIBaseController):

    @coroutine
    def post(self):
        data = self.data
        a = int(data['a'])
        b = int(data['b'])
        self.response(dict(a=a, b=b, val=a * b))
