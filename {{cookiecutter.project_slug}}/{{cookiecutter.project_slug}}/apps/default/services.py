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
{%- if cookiecutter.use_database == 'y' %}
from {{cookiecutter.project_slug}}.storage.postgres import PostgreSQLConnector
from {{cookiecutter.project_slug}}.storage.postgres import connection as database_connection
from {{cookiecutter.project_slug}}.common.database import fetchall_as_dict
from tornado.gen import coroutine, Return

@coroutine
@database_connection(name="master")
def add(db, x, y):
    r = yield db.execute('SELECT %s::bigint + %s::bigint AS PING, now()::TEXT as TS', (int(x), int(y)))
    raise Return(fetchall_as_dict(r))

{%- endif %}
