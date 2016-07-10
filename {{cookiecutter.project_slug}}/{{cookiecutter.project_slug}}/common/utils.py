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
#                              5 Apr, 2016
#
from os.path import dirname, join as path_join
import shlex
import subprocess

def try_get_value(d, path, null_value=None):

    current, nodes = d, path.split('.')

    while nodes:
        if not isinstance(current, dict):
            return null_value
        key = nodes.pop(0)
        if key not in current:
            return null_value
        current = current[key]

    return current


def get_webapp_root(name):
    abspath = path_join(dirname(dirname(__file__)),
                        'static/webapp/apps', name)
    return abspath


def async_run_command(command):

    LOG.debug('invoking command "%s"' % command)
    io_loop = ioloop.IOLoop.instance()
    pipe = subprocess.Popen(shlex.split(command),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            close_fds=True)
    command_future = Future()

    def _result(fd, result):
        try:
            command_future.set_result(pipe.stdout)
        except Exception, e:
            LOG.error(e)
            command_future.set_exception(e)
        finally:
            io_loop.remove_handler(fd)

    io_loop.add_handler(pipe.stdout.fileno(), _result, io_loop.READ)
    return command_future
