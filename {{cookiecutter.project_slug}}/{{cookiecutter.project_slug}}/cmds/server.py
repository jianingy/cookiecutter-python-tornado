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
from {{cookiecutter.project_slug}}.application import Application
{%- if cookiecutter.use_database == 'y' %}
from {{cookiecutter.project_slug}}.storage import postgres
{%- endif %}
from tornado.options import (define as tornado_define,
                             options as tornado_options,
                             parse_config_file)
import logging
import tornado.ioloop
import tornado.httpserver

tornado_define('workers', default=0,
               help="num of workers", type=int)
{%- if cookiecutter.use_database == 'y' %}
tornado_define('postgres-uri', default='postgres:///',
               help="postgresql connection uri")
tornado_define('postgres-max-pool-size', default=4,
               help='maximum connection pool size of PostgreSQL')
tornado_define('postgres-reconnect-interval', default=5,
               help='maximum connection pool size of PostgreSQL')
{%- endif %}
tornado_define("config", type=str, help="path to config file",
               callback=lambda path: parse_config_file(path, final=False))
LOG = logging.getLogger('tornado.application')  # noqa


def main():
    from tornado.log import enable_pretty_logging
    enable_pretty_logging()
    tornado.options.parse_command_line()

    app = Application()
    bind_address, bind_port = tornado_options.bind.split(':', 1)

    if tornado_options.debug:
        app.listen(int(bind_port), address=bind_address)
    else:
        server = tornado.httpserver.HTTPServer(app)
        server.bind(int(bind_port), address=bind_address)
        server.start(tornado_options.workers)
    io_loop = tornado.ioloop.IOLoop.instance()
    {%- if cookiecutter.use_database == 'y' %}
    postgres_settings = dict(
        max_pool_size=tornado_options.postgres_max_pool_size,
        reconnect_interval=tornado_options.postgres_reconnect_interval
    )
    postgres.init(tornado_options.postgres_uri, io_loop=io_loop,
                  **postgres_settings)
    {%- endif %}
    io_loop.start()
