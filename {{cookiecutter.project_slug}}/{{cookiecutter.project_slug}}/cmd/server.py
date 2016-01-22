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
from tornado.options import options as tornado_options
import logging
import tornado.ioloop
import tornado.httpserver


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
        server.start(0)

    tornado.ioloop.IOLoop.instance().start()
