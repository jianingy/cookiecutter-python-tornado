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
from tornado.options import (define as tornado_define,
                             options as tornado_options)
from urlparse import urlparse
import functools
import momoko
import logging
import tornado.ioloop

tornado_define('postgres-uri', default='postgres:///',
               help="postgresql connection uri")
tornado_define('postgres-max-pool-size', default=4,
               help='maximum connection pool size of PostgreSQL')
tornado_define('postgres-reconnect-interval', default=5,
               help='maximum connection pool size of PostgreSQL')


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
    def connect(cls, **kwd):
        r = urlparse(tornado_options.postgres_uri)
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
        interval = kwd.get('reconnect_interval',
                           tornado_options.postgres_reconnect_interval)
        size = kwd.get('max_pool_size',
                       tornado_options.postgres_max_pool_size)
        LOG.info('Database connection string is %s' % dsn)
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


def connection(method=None, name="master"):

    def wrapper(function):

        @functools.wraps(function)
        def f(*args, **kwds):
            db = PostgreSQLConnector.instance(name).connection()
            return function(db, *args, **kwds)
        return f

    return wrapper
