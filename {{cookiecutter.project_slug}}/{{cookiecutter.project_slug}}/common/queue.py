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
#                             10 Jul, 2016
#
from json import loads as json_decode
from tornado.gen import maybe_future
from urlparse import urlparse
import os
import stormed
import tornado
import logging

LOG = logging.getLogger('tornado.application')


class QueueConsumer(object):

    def __init__(self, name, on_message, **kwargs):
        self._queue_name = name
        self._durable = kwargs.get('durable', True)
        self._prefetch_count = kwargs.get('prefetch_count', 1)
        self._exchange = None
        self._bound = False
        self._initialized = False
        self._on_message = on_message

    def _consume(self, msg):
        io_loop = tornado.ioloop.IOLoop.instance()

        if msg.content_type != 'application/json':
            LOG.warn('invalid content-type header.'
                     ' only json content is acceptable.'
                     ' message rejected.')
            msg.reject(requeue=False)
            return False

        try:
            data = json_decode(msg.body)
        except ValueError as e:
            msg.reject(requeue=False)
            LOG.warn('malformed json message: %s. reason: %s '
                     'message rejected.' % (msg.body, e))
        else:
            future = maybe_future(self._on_message(data))
            io_loop.add_future(future, lambda f: self._ack(f, msg))

    def _setup(self):
        ch = self._conn.channel()
        ch.queue_declare(queue=self._queue_name, durable=self._durable)
        ch.qos(prefetch_count=self._prefetch_count)
        ch.consume(self._queue_name, self._consume)
        if self._exchange:
            ch.queue_bind(exchange=self._exchange, queue=self._queue_name)
        self._initialized = True

    def _ack(self, future, msg):
        try:
            future.result()
            msg.ack()
        except Exception as e:
            LOG.warn('error on processing this message: %s.'
                     ' message has been push back to the queue' % e)
            msg.reject()

    def bind(self, exchange):
        if self._initialized:
            raise RuntimeError('queue already initialized')
        self._exchange = exchange

    def connect(self, uri):
        r = urlparse(uri)
        if r.scheme.lower() != 'amqp':
            raise AMQPConnectorError('uri should starts with amqp://')
        self._conn = stormed.Connection(host=r.hostname,
                                        port=int(r.port or 5672),
                                        username=r.username,
                                        password=r.password,
                                        vhost=r.path)
        self._conn.connect(self._setup)
