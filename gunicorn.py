# Gunicorn configuration file Sample:
# https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
#
# cd /srv/www/moin/wiki ;/srv/www/moin/env/bin/gunicorn -c /srv/www/moin/etc/gunicorn_config.py -u www-data moin:appx
#

#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.
#
#   backlog - The number of pending connections. This refers
#       to the number of clients that can be waiting to be
#       served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should
#       only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048
#       range.
#

# bind = 'unix:///srv/www/moin/var/gunicorn.sock'
bind = '0.0.0.0:3301'
backlog = 2048

#
# Worker processes
#
workers = 4
worker_class = 'gevent'
worker_connections = 100
timeout = 30
keepalive = 2

#
# Server mechanics
#
# daemon = True
# pidfile = '/srv/www/moin/var/gunicorn.pid'
# umask = 0
# user = 'www-data'
# group = 'www-data'
# tmp_upload_dir = None

daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None


#
#   Logging
#
#   logfile - The path to a log file to write to.
#
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output
#
#       A string of "debug", "info", "warning", "error", "critical"
#

errorlog = '/srv/www/moin/var/error-gunicorn.log'
# errorlog = '-'
loglevel = 'info'
# accesslog = '/srv/www/moin/var/gunicorn_log/access.log'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

proc_name = None

#
# Server hooks
#
#   post_fork - Called just after a worker has been forked.
#
#       A callable that takes a server and worker instance
#       as arguments.
#
#   pre_fork - Called just prior to forking the worker subprocess.
#
#       A callable that accepts the same arguments as after_fork
#
#   pre_exec - Called just prior to forking off a secondary
#       master process during things like config reloading.
#
#       A callable that takes a server instance as the sole argument.
#


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    # get traceback info
    import threading
    import sys
    import traceback
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""),
                                            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                                                        lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
