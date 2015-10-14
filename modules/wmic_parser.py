#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
(C) Copyright [2015] InfoSec Consulting, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

         ...
    .:::|#:#|::::.
 .:::::|##|##|::::::.
 .::::|##|:|##|:::::.
  ::::|#|:::|#|:::::
  ::::|#|:::|#|:::::
  ::::|##|:|##|:::::
  ::::.|#|:|#|.:::::
  ::|####|::|####|::
  :|###|:|##|:|###|:
  |###|::|##|::|###|
  |#|::|##||##|::|#|
  |#|:|##|::|##|:|#|
  |#|##|::::::|##|#|
   |#|::::::::::|#|
    ::::::::::::::
      ::::::::::
       ::::::::
        ::::::
          ::
"""

__author__ = 'Avery Rozar'

from locale import getdefaultlocale
from subprocess import PIPE, Popen


def wmic_query(domain, username, password, host, query):
  try:
    encoding = getdefaultlocale()[1]
    wmi_query = Popen(['wmic',
                       '-U',
                       '%s/%s%%%s' % (domain, username, password),
                       '//%s' % host,
                       '%s' % query], stdout=PIPE)
    wmi_reply = wmi_query.communicate()[0]
    wmi_reply_list = wmi_reply.decode(encoding).split('\n')
    keys = wmi_reply_list[1].split('|')
    values = wmi_reply_list[2].split('|')
    wmi_op_dict = dict(zip(keys, values))
    return wmi_op_dict
  except IndexError:
    print('Something went horribly wrong, try a different query.')
    return 1
