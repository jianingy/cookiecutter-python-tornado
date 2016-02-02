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
from {{cookiecutter.project_slug}}.common.app import TornadoDaemonMixin
from datetime import timedelta
import tornado.ioloop


class Daemon(TornadoDaemonMixin):

    def hello(self):
        print "#%s says hello" % self.tid
        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.call_later(1, self.hello)

    def before_run(self, io_loop):
        io_loop.call_later(1, self.hello)
        io_loop.add_timeout(timedelta(seconds=5), lambda: io_loop.stop())


def run():
    Daemon().run()
