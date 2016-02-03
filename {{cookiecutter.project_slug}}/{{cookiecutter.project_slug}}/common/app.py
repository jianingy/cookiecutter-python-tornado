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

from os.path import join as path_join, dirname
from tornado.options import (define as tornado_define,
                             options as tornado_options,
                             parse_config_file)
from tornado.process import fork_processes
from tornado.util import import_object
from warnings import warn
import logging
import logging.config
import tornado.web
import tornado.ioloop
import tornado.httpserver


tornado_define('workers', default=1,
               help="num of workers", type=int)
tornado_define('debug', default=False, help="debug", type=bool)
tornado_define("logging-config", default='',
               help="path to logging config file")
tornado_define("config", type=str, help="path to config file",
               callback=lambda path: parse_config_file(path, final=False))

LOG = logging.getLogger('tornado.application')
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colorlog': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s<%(process)d>[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s%(reset)s',
            'datefmt': '%y%m%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colorlog',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'app.biz': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


class BaseCommand(object):

    def enable_logging(self):
        if tornado_options.debug:
            level = 'DEBUG'
        else:
            level = tornado_options.logging.upper()
        logging.config.dictConfig(LOGGING_CONFIG)
        if tornado_options.logging_config:
            logging.config.fileConfig(tornado_options.logging_config,
                                      disable_existing_loggers=False)
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, level))


class TornadoServerMixin(BaseCommand):

    def before_server_start(self, io_loop):
        pass

    def start_server(self):
        tornado_define('bind', default='127.0.0.1:8000',
                       help="server bind address")
        tornado.options.parse_command_line()
        self.enable_logging()
        bind_address, bind_port = tornado_options.bind.split(':', 1)

        if tornado_options.debug:
            self.listen(int(bind_port), address=bind_address)
        else:
            server = tornado.httpserver.HTTPServer(self)
            server.bind(int(bind_port), address=bind_address)
            server.start(tornado_options.workers)
        io_loop = tornado.ioloop.IOLoop.instance()
        self.before_server_start(io_loop)
        io_loop.start()


class TornadoDaemonMixin(BaseCommand):

    def before_run(self, io_loop):
        pass

    def run(self):
        tornado.options.parse_command_line()
        self.enable_logging()
        self.tid = 0
        if tornado_options.workers != 1:
            # fork_process never return in parent process
            # instead it will exit the program when all its
            # children quit.
            self.tid = fork_processes(tornado_options.workers)
            LOG.info('process #%s started' % self.tid)

        io_loop = tornado.ioloop.IOLoop.instance()
        self.before_run(io_loop)
        io_loop.start()


class WebApplication(tornado.web.Application):

    enabled_apps = []
    ui_modules = []

    def __init__(self):
        server_root = dirname(__file__)
        webapp_settings = dict(
            debug=tornado_options.debug,
            autoreload=tornado_options.debug,
            ui_modules=self.ui_modules,
            template_path=path_join(server_root, "templates"),
            static_path=path_join(server_root, "static"),
        )

        for app in self.enabled_apps:
            try:
                import_object('%s.controllers' % app)
            except Exception as e:
                warn('Failed to load app %s: %s' % (app, e))
        route = import_object('{{cookiecutter.project_slug}}.common.route')
        controllers = route.route.get_routes()
        tornado.web.Application.__init__(self, controllers, **webapp_settings)


class ApiApplication(tornado.web.Application):

    enabled_apps = []

    def __init__(self):
        webapp_settings = dict(
            debug=tornado_options.debug,
            autoreload=tornado_options.debug,
        )
        for app in self.enabled_apps:
            try:
                import_object('%s.controllers' % app)
            except Exception as e:
                warn('Failed to load app %s: %s' % (app, e))
        route = import_object('{{cookiecutter.project_slug}}.common.route')
        controllers = route.route.get_routes()
        tornado.web.Application.__init__(self, controllers, **webapp_settings)
