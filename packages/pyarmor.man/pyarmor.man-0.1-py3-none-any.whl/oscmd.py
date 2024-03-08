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
#  @File: oscmd.py
#
#  @Author: Jondy Zhao(pyarmor@163.com)
#
#  @Create Date: Thu Jan  4 20:28:28 CST 2024
#
"""Execute os command in backgroud

Examples:
    Run `ls` command in the current path

    >>> from oscmd import Command
    >>> c = Command(['ls', '-l'])
    >>> c.run()
    >>> print(c.stdout)
"""
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from threading import Thread


class Command(object):
    """Execute any shell command in the backgroud

    Attributes:
        stdout (list(str))
    """

    def __init__(self, args):
        self.args = args
        self.stdout = []
        self._proc = None
        self._thread = None

    @property
    def rc(self):
        """int: Return code of running process"""
        return self._proc and getattr(self._proc, 'returncode', None)

    def _read_proc(self, proc):
        while True:
            lines = proc.stdout.readline()
            if not lines:
                try:
                    proc.communicate(timeout=3.0)
                except TimeoutExpired:
                    self.stdout.append('TimeoutExpired')
                    proc.kill()
                    proc.communicate()
                break
            self.stdout.append(lines)

    def run(self, args=None, cwd=None, encoding=None):
        """Run shell command

        Returns:
            True if process starts
            None if faild to start command, store error message to self.stdout
        """
        args = self.args if args is None else args
        try:
            self._proc = Popen(args, stderr=STDOUT, stdout=PIPE, cwd=cwd,
                               bufsize=1, text=True, encoding=encoding)
            self._thread = Thread(target=self._read_proc, args=(self._proc,))
            self._thread.start()
            return True
        except OSError as e:
            self.stdout.append(str(e))

    def kill(self, silent=True):
        """Kill the running process

        Returns:
            None if success else str for error message
        """
        if self._proc:
            try:
                self._proc.kill()
            except Exception as e:
                return str(e)

    def clean(self):
        """Kill proc if proc is running else do nothing"""
        if self._proc and self._proc.returncode is None:
            self.kill()
