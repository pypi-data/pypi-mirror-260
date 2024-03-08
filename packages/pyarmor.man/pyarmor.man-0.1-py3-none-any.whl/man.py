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
#  @File: man.py
#
#  @Author: Jondy Zhao(pyarmor@163.com)
#
#  @Create Date: Thu Jan  24 18:25:28 CST 2024
#
import logging

from urllib.request import urlopen
from urllib.error import HTTPError

def _get_remote_file(url, timeout=6.0):
    try:
        res = urlopen(url, timeout=timeout)
    except Exception:
        from ssl import _create_unverified_context as create_context
        res = urlopen(url, timeout=timeout, context=create_context())

    return res


def check_and_update_data(cfg):
    """Check and download server data

    First download index.json from cfg.get('man', 'index')
    If return HTTP 404, then print hint to upgrade pyarmor.man

    Then parse index.json, download necessary data if necessary
    """
    url = cfg.get('man', 'index')
    try:
        res = _get_remote_file(url)
    except HTTPError as e:
        res = e

    if res.status in (200, 301, 302, 307, 308):
        return True

    logging.error('Could not download data from server: %s', res.reason)
    if res.status == 404:
        logging.error('Please update pyarmor.man to latest version by')
        logging.error('   pip install -U pyarmor.man')
