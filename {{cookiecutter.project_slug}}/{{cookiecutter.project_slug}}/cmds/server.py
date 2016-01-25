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
from {{cookiecutter.project_slug}}.persistent import postgres
{%- endif %}
from tornado.options import (define as tornado_define,
                             options as tornado_options,
                             parse_config_file)
import logging
import tornado.ioloop
import tornado.httpserver

tornado_define('workers', default=0,
               help="num of workers", type=int)
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
    postgres.init(io_loop)
    {%- endif %}
    io_loop.start()
