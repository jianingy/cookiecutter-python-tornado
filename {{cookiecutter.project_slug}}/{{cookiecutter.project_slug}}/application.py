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
#     oo    oo  'oo OOOO-| oo\\_   ~o~~o~
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                             21 Jan, 2016
#

from {{cookiecutter.project_slug}}.common.route import route
{%- if cookiecutter.use_database %}
from {{cookiecutter.project_slug}}.persistent.postgres import PostgreSQLConnector
{%- endif %}
from tornado.options import (define as tornado_define,
                             options as tornado_options)
from os.path import join as path_join, dirname
from tornado.util import import_object
import re
import tornado.web
import logging

tornado_define('debug', default=False, help="debug", type=bool)
tornado_define('bind', default='127.0.0.1:8000', help="server bind address")
tornado_define('enabled-apps',
               default=['{{cookiecutter.project_slug}}.app.default'],
               multiple=True, help="server bind address")

LOG = logging.getLogger('tornado.application')


class Application(tornado.web.Application):

    def __init__(self):

        # Load app ui modules
        ui_modules_map = {}
        match_ui_modules = re.compile('[A-Z]\w+')

        for app_name in tornado_options.enabled_apps:
            try:
                ui_modules = import_object('%s.ui_modules' % app_name)
            except ImportError:
                # Just ignore in case the app dont have ui_modules
                continue

            for name in [x for x in dir(ui_modules) if match_ui_modules(x)]:
                thing = getattr(ui_modules, name)
                try:
                    if issubclass(thing, tornado.web.UIModule):
                        ui_modules_map[name] = thing
                except TypeError:
                    # most likely a builtin class or something
                    pass

        server_root = dirname(__file__)
        webapp_settings = dict(
            debug=tornado_options.debug,
            autoreload=tornado_options.debug,
            ui_modules=ui_modules_map,
            template_path=path_join(server_root, "template"),
            static_path=path_join(server_root, "static"),
        )
        controllers = route.get_routes()
        tornado.web.Application.__init__(self, controllers, **webapp_settings)
        {%- if cookiecutter.use_database %}
        database = PostgreSQLConnector()
        database.connect()
        {%- endif %}


# Load apps during evaluation. So tornado_define can be
# used in apps' controllers
[import_object('%s.controllers' % app) for app in tornado_options.enabled_apps]
