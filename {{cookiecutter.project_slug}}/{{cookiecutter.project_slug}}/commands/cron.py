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
from {{cookiecutter.project_slug}}.common.app import ConsoleApplication, run_app
from datetime import timedelta
from tornado.gen import coroutine, sleep
import tornado.ioloop


class CronApp(ConsoleApplication):

    @coroutine
    def run(self):
        while True:
            print "#%s says hello" % self.tid
            yield sleep(3)


def run():
    run_app(CronApp)
