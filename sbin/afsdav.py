"""
AFS WebDAV Gateway: PAG sandbox, other krb5 utils
"""

from os.path import abspath, dirname
BASE = abspath(abspath(dirname(__file__))+'/../')
RUN = BASE + '/run'

import os, signal
from subprocess import Popen, PIPE, STDOUT
from tempfile import mkstemp

def kinit(username, password, cfile=None):
    kc = cfile
    if kc is None:
        kc = mkstemp();
        os.close(kc[0]);
        kc = kc[1]
    p2fr, p2fw = os.pipe()
    f2pr, f2pw = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.dup2(p2fr, 0)
        os.dup2(f2pw, 1)
        os.dup2(f2pw, 2)
        os.execv('/usr/bin/kinit', ['kinit', '-l', '3d', '-c', kc, username])
    else:
        os.close(p2fr)
        os.close(f2pw)
        os.fdopen(p2fw,'w').write('%s\n' % password)
        pres = os.waitpid(pid, 0)
        if pres[1] == 0:
            # return ticket kc
            return kc
        else:
            # execv failure
            if cfile is None:
                # remove ticket kc
                os.unlink(kc)

def aklog(cfile, cells=['athena.mit.edu', 'sipb.mit.edu']):
    Popen(['/usr/bin/aklog', '-setpag', '-noprdb'], env={'KRB5CCNAME': cfile}, close_fds=True).wait()
    Popen(['/usr/bin/aklog', '-noprdb'] + cells, env={'KRB5CCNAME': cfile}, close_fds=True).wait()
    return True

from time import strptime, gmtime
from calendar import timegm
strptoken = lambda s: timegm(strptime(str(gmtime().tm_year) + ' ' + s, '%Y %b %d %H:%M'))

def tokens_until(f):
    r = []
    for line in file(f).readlines():
        line = line.strip()
        if 'Expires' in line:
            r += [strptoken(line.split('[Expires ', 1)[-1][:-1])]
    return r and min(r) or 0

def ticket_start(username, ticket):
    # prepare env
    usernamef = username.replace('/', '.')
    env = dict(os.environ)
    env.update(DAV_USER=username, DAV_USERF=usernamef)

    # remove target PID file
    try: os.unlink('%s/%s.pid' % (RUN, usernamef))
    except Exception: pass

    def preexec_fn():
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    r = aklog(ticket)
    if r:
        p = Popen(args=([BASE + '/sbin/lighttpd'] +
                        ['-D', '-f', BASE + '/etc/backend.conf', '-m', BASE + '/lib/lighttpd']),
                  preexec_fn=preexec_fn,
                  cwd=BASE,
                  env=env,
                  close_fds=True)

        f_pid = file('%s/%s.pid' % (RUN, usernamef), 'w')
        f_pid.write('%d' % p.pid)
        f_pid.close()

        ttl_p = '%s/%s.ttl' % (RUN, usernamef)
        tok_p = '%s/%s.tok' % (RUN, usernamef)
        p_tok = Popen(['/usr/bin/tokens'], stdout=PIPE)
        file(tok_p, 'w').write(p_tok.stdout.read())
        p_tok.stdout.close()
        p_tok.wait()
        file(ttl_p, 'w').write(str(tokens_until(tok_p)))
        stat_userdir(username)
        return p

def stat_userdir(user):
    try: return os.stat(os.path.join('/mit', user.partition('@')[0].partition('.')[0].lower()))
    except Exception: pass

def pid_environ(pid):
    try:
        f = file('/proc/%s/environ' % str(pid), 'r')
        d = f.read().split(chr(0))
        d = map(lambda x: len(x.split('=')) > 1 and [x.split('=')[0], '='.join(x.split('=')[1:])], d)
        return dict(filter(lambda x: type(x) is list, d))
    except IOError, e:
        pass
