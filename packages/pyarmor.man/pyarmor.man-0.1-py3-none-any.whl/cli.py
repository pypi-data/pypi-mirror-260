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
#  @File: cli.py
#
#  @Author: Jondy Zhao(pyarmor@163.com)
#
#  @Create Date: Thu Jan  4 20:28:28 CST 2024
#
import argparse
import configparser
import logging
import os
import sys

from . import __version__
from .server import start_server
from .man import check_and_update_data

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'default.cfg')


def _fix_up_win_console_freeze():
    try:
        from ctypes import windll
        from win32api import GetStdHandle, SetConsoleTitle
        SetConsoleTitle("Pyarmor Man")
        # Disable quick edit in CMD, as it can freeze the application
        handle = GetStdHandle(-10)
        if handle != -1 and handle is not None:
            windll.kernel32.SetConsoleMode(handle, 128)
    except Exception:
        pass


def main_parser():
    parser = argparse.ArgumentParser(
        prog='pyarmor-man',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('-v', '--version', action='version',
                        version=__version__)
    parser.add_argument('-p', '--port', type=int, default=10096,
                        help='Serve port, default is 10096')
    parser.add_argument('-H', '--host', default='localhost',
                        help='Bind host, default is localhost')
    parser.add_argument('-n', '--no-browser', action='store_true',
                        help='Do not open web browser')
    parser.add_argument('-i', '--index', default='',
                        help='Index page, default is index.html')
    parser.add_argument('-e', '--encoding',
                        help='Specify encoding for configuration file')
    parser.add_argument('-c', '--cached', action='store_true',
                        help='Using cached data, do not download server data')
    return parser


def main_entry(args):
    cfg = configparser.ConfigParser(
        empty_lines_in_values=False,
        interpolation=configparser.ExtendedInterpolation(),
    )
    cfg.read([DEFAULT_CONFIG_FILE], encoding=args.encoding)

    if sys.platform == 'win32':
        _fix_up_win_console_freeze()

    if args.cached or not check_and_update_data(cfg):
        logging.warning('Using cached data, it may be out of date')

    logging.info("Serving HTTP on %s port %s ...", args.host, args.port)
    start_server(args.host, args.port, no_browser=args.no_browser, cfg=cfg)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-8s %(message)s',
    )
    try:
        parser = main_parser()
        args = parser.parse_args(sys.argv[1:])
        main_entry(args)
    except KeyboardInterrupt:
        logging.info('Keyboard interrupt received, exiting.')


if __name__ == '__main__':
    main()
