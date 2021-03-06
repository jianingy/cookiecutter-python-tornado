# -*- coding: utf-8 -*-
#
# This piece of code is written by
#    Jianing Yang <jianingy.yang@gmail.com>
# with love and passion!
#
#        H A P P Y    H A C K I N G !
#              _____               ______
#     ____====  ]OO|_n_n__][.      |    |
#    [________]_|__|________)<     |YANG|
#     oo    oo  'oo OOOO-| oo\\_   ~o~~o~
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                              2 Feb, 2016
#
from {{cookiecutter.project_slug}}.common.app import WebApplication, run_app
{%- if cookiecutter.use_database == 'y' %}
from {{cookiecutter.project_slug}}.common import postgres
{%- endif %}
from tornado.options import (define as tornado_define,
                             options as tornado_options)
import logging

LOG = logging.getLogger('tornado.application')

{%- if cookiecutter.use_database == 'y' %}
tornado_define('postgres-uri', default='postgres:///', group='database',
               help="postgresql connection uri")
tornado_define('postgres-max-pool-size', default=4, group='database',
               help='maximum connection pool size of PostgreSQL')
tornado_define('postgres-reconnect-interval', default=5, group='database',
               help='maximum connection pool size of PostgreSQL')
{%- endif %}


class WebAppServer(WebApplication):

    enabled_apps = ['{{cookiecutter.project_slug}}.apps.default']

    def before_run(self, io_loop):
        LOG.info('starting default server ...')
        {%- if cookiecutter.use_database == 'y' %}
        postgres_settings = dict(
            max_pool_size=tornado_options.postgres_max_pool_size,
            reconnect_interval=tornado_options.postgres_reconnect_interval
        )
        f = postgres.init(tornado_options.postgres_uri, io_loop=io_loop,
                          **postgres_settings)
        io_loop.add_future(f, lambda x: x)
        {%- endif %}


def run():
    run_app(WebAppServer)
