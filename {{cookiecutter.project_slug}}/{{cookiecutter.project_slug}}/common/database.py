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


def fetchall_as_dict(cursor):
    """fetch all cursor results and returns them as a list of dicts"""
    names = [x[0] for x in cursor.description]
    rows = cursor.fetchall()
    if rows:
        return [dict(zip(names, row)) for row in rows]
    else:
        return []


def fetchone_as_dict(cursor):
    """fetch one cursor results and returns them as a list of dicts"""
    names = [x[0] for x in cursor.description]
    row = cursor.fetchone()
    if row:
        return dict(zip(names, row))
    else:
        return None
