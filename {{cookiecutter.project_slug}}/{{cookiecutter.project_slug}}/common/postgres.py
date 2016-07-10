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
#     oo    oo  'oo OOOO-| oo\\_   ~o~~~o~
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                             22 Jan, 2016
#
from tornado.gen import coroutine
from urlparse import urlparse
from tornado.options import (define as tornado_define,
                             options as tornado_options)
import functools
import momoko
import logging
import tornado.ioloop

LOG = logging.getLogger('tornado.application')


class PostgreSQLConnectorError(Exception):
    pass


class PostgreSQLConnector(object):

    _instances = dict()

    @staticmethod
    def instance(name='master'):
        if name not in PostgreSQLConnector._instances:
            PostgreSQLConnector._instances[name] = PostgreSQLConnector()
        return PostgreSQLConnector._instances[name]

    @classmethod
    def connection(cls):
        if not hasattr(cls, '_pool') or not cls._pool:
            raise PostgreSQLConnectorError('not connected')
        return cls._pool

    @classmethod
    @coroutine
    def connect(cls, uri, **kwd):
        r = urlparse(uri)
        if r.scheme.lower() != 'postgres':
            raise PostgreSQLConnector('uri should starts with postgres://')

        io_loop = tornado.ioloop.IOLoop.instance()
        dsn_format = ('host={host} port={port} dbname={dbname}'
                      ' user={user} password={password}')
        dsn = dsn_format.format(host=r.hostname or 'localhost',
                                port=r.port or 5432,
                                user=r.username,
                                password=r.password,
                                dbname=r.path.lstrip('/') or r.username)
        interval = kwd.get('reconnect_interval', 5)
        size = kwd.get('max_pool_size', 4)
        LOG.info('postgresql connection string is %s' % dsn)
        cls._pool = momoko.Pool(
            dsn=dsn,
            reconnect_interval=interval,
            size=size,
            ioloop=io_loop,
        )

        yield cls._pool.connect()

    @classmethod
    def disconnect(cls):
        return cls.connection().close()


class PostgreSQLEngine(object):

    @staticmethod
    def register_options(name='master'):
        opt_name = '' if name == 'master' else '-%s' % name
        tornado_define('postgres%s-uri' % opt_name,
                       default='postgres:///',
                       group='%s database' % name,
                       help="postgresql connection uri for %s" % name)
        tornado_define('postgres%s-max-pool-size' % opt_name,
                       default=4,
                       group='%s database' % name,
                       help='connection pool size for %s ' % name)
        tornado_define('postgres%s-reconnect-interval' % opt_name,
                       default=5,
                       group='%s database' % name,
                       help='reconnect interval for %s' % name)

    @staticmethod
    def start(name, io_loop=None):
        opt_name = '' if name == 'master' else '-%s' % name
        postgres_settings = tornado_options.group_dict('%s database' % name)
        instance = PostgreSQLConnector.instance(name)
        uri = postgres_settings['postgres%s-uri' % opt_name]
        if not io_loop:
            io_loop = tornado.ioloop.IOLoop.instance()
        def _start():
            return instance.connect(uri, **postgres_settings)
        #io_loop.add_future(f, _done)
        io_loop.run_sync(_start)


def with_postgres(method=None, name="master"):

    def wrapper(function):

        @functools.wraps(function)
        def f(*args, **kwargs):
            db = PostgreSQLConnector.instance(name).connection()
            return function(db, *args, **kwargs)
        return f

    return wrapper
