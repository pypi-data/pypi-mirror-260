#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2024 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      Pyarmor.Man                                          #
#                                                           #
#      Version: 1.0 -                                       #
#                                                           #
#############################################################
#
#
#  @File: handler.py
#
#  @Author: Jondy Zhao(pyarmor@163.com)
#
#  @Create Date:  Wed Jan 24 18:20:26 CST 2024
#
import glob
import json
import os
import sys

from fnmatch import fnmatch
from shlex import quote

from . import __version__
from .oscmd import Command


class BaseHandler(object):

    def __init__(self, config):
        self.cfg = config
        self.children = []

    def dispatch(self, path, args):
        i = path.find('/')
        if i == -1:
            if hasattr(self, 'do_' + path):
                return getattr(self, 'do_' + path)(args)
            raise RuntimeError('No route for %s', path)
        else:
            name = path[:i]
            for handler in self.children:
                if handler.name == name:
                    return handler.dispatch(path[i+1:], args)
            raise RuntimeError('No route for %s', name)

    def _check_arg(self, name, value, valids=None, invalids=None, types=None):
        if value in (None, ''):
            raise RuntimeError('Missing argument "%s"' % name)
        if valids is not None and value not in valids:
            raise RuntimeError('Invalid argument "%s"' % name)
        if invalids is not None and value in invalids:
            raise RuntimeError('Invalid argument "%s"' % name)
        if types is not None and not isinstance(value, types):
            raise RuntimeError('Invalid argument "%s"' % name)

    def _check_path(self, path):
        if not os.path.exists(path):
            raise RuntimeError('This path %s does not exists' % path)

    def _format_path(self, path):
        return path.strip('/') if sys.platform == 'win32' else path


class SystemHandler(BaseHandler):

    def do_info(self, args=None):
        from platform import python_implementation
        uname = os.uname()
        data = {
            'platform': uname.sysname,
            'arch': uname.machine,
            'system': uname.version,
            'server': 'Pyarmor.Man/' + __version__,
            'python': {
                'version': '%s.%s.%s' % sys.version_info[:3],
                'implementation': python_implementation(),
                'executable': sys.executable,
            }
        }
        return data


class DirectoryHandler(BaseHandler):

    def __init__(self, config):
        super().__init__(config)

    def do_get(self, args=None):
        return os.path.normpath(os.getcwd())

    def do_make(self, args):
        self._check_arg('path', args)

        if not os.path.exists(args):
            os.makedirs(args)
        return os.path.abspath(args)

    def do_remove(self, args):
        self._check_arg('path', args, invalids=['.', '/'])
        self._check_path(args)

        os.rmdir(args)
        return os.path.abspath(args)

    def do_list(self, args):
        path = os.path.expandvars(args.get('path', '/'))
        if sys.platform == 'win32':
            if path == '/':
                from ctypes import cdll
                drives = cdll.kernel32.GetLogicalDrives()
                result = []
                for i in range(26):
                    if drives & 1:
                        result.append(chr(i + 65) + ':')
                    drives >>= 1
                return {
                    'path': path,
                    'dirs': result,
                    'files': []
                }
            if path == '@':
                return {
                    'path': path,
                    'dirs': ['/',
                             '/' + os.path.expanduser('~').replace('\\', '/')],
                    'files': []
                }
            if path[0] == '/':
                path = path[1:]
            if len(path) == 2 and path[1] == ':':
                path += '/'

        if path == '@':
            return {
                'path': path,
                'dirs': ['/', os.path.expanduser('~')],
                'files': []
            }

        path = os.path.normpath(path)
        if not os.path.exists(path):
            raise RuntimeError('No %s found' % path)

        dirs = []
        files = []
        pat = args.get('pattern', '*')
        for x in glob.glob(os.path.join(path, '*')):
            if os.path.isdir(x):
                dirs.append(os.path.basename(x).replace('\\', '/'))
            elif pat == '*' or fnmatch(os.path.basename(x), pat):
                files.append(os.path.basename(x).replace('\\', '/'))
        dirs.sort(key=str.lower)
        files.sort(key=str.lower)
        return {
            'path': os.path.abspath(path).replace('\\', '/'),
            'dirs': dirs,
            'files': files,
        }


class AppHandler(BaseHandler):

    PYARMOR = [sys.executable, '-m', 'pyarmor.cli']
    PYTHON = [sys.executable]

    def __init__(self, config):
        super().__init__(config)
        self.commander = None

    def do_info(self, args=None):
        from pyarmor.cli.context import Context
        try:
            from pyarmor.cli.core import __VERSION__ as corever
        except ImportError:
            corever = _('not installed')
        home = os.path.normpath(os.path.expanduser('~/.pyarmor'))
        ctx = Context(home)
        licinfo = ctx.license_info
        lictype = 'basic' if licinfo['features'] == 1 else \
            _('Pyarmor Pro') if licinfo['features'] == 7 else \
            _('Pyarmor Group') if licinfo['features'] == 15 else \
            _('Pyarmor Trial') if licinfo['token'] == 0 else _('Unknown')
        return {
            'pyarmor': ctx.version_info(verbose=0),
            'core': corever,
            'license': {
                'id': licinfo['licno'][-6:],
                'type': lictype,
                'regname': licinfo['regname'],
                'product': licinfo['product']
            }
        }

    def do_run(self, args):
        if self.commander:
            self.commander.clean()
        cmdargs = (self.PYARMOR[:] if args['cmd'] == 'pyarmor' else
                   self.PYTHON[:] if args['cmd'] == 'python' else
                   [args['cmd']])
        for opt in args['opts']:
            cmdargs.extend([x.strip() for x in opt.split(' ', 1)])
        cmdargs.extend(args['args'])
        self.commander = Command(cmdargs)
        running = self.commander.run()
        cmdline = ' '.join([quote(x) for x in cmdargs]) + '\n'
        return {
            'running': running,
            'msg': cmdline if running else ''.join(self.commander.stdout)
        }

    def do_kill(self, args=None):
        if self.commander:
            return self.commander.kill()

    def do_status(self, args=None):
        return self.commander and self.commander.rc

    def do_output(self, args=None):
        if self.commander:
            index = args.get('index', 0)
            return {
                'lines': self.commander.stdout[index:],
                'rc': self.commander.rc
            }
        raise RuntimeError(_('No running process'))


class ManHandler(BaseHandler):

    def __init__(self, config):
        super().__init__(config)

    def do_info(self, args=None):
        datapath = os.path.join(os.path.dirname(__file__), 'data')
        filename = 'pyarmor.json'
        with open(os.path.join(datapath, filename)) as f:
            return json.load(f)

    def do_user(self, args=None):
        datapath = os.path.join(os.path.dirname(__file__), 'data')
        filename = 'user.json'
        with open(os.path.join(datapath, filename)) as f:
            return json.load(f)

    def do_faq(self, args=None):
        datapath = os.path.join(os.path.dirname(__file__), 'data')
        filename = 'questions.json'
        with open(os.path.join(datapath, filename)) as f:
            return json.load(f)

    def do_err(self, args=None):
        datapath = os.path.join(os.path.dirname(__file__), 'data')
        filename = 'errors.json'
        with open(os.path.join(datapath, filename)) as f:
            return json.load(f)

    def do_issue(self, args=None):
        datapath = os.path.join(os.path.dirname(__file__), 'data')
        filename = 'issues.json'
        with open(os.path.join(datapath, filename)) as f:
            return json.load(f)
