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

import subprocess
import os
from time import sleep
import re


def nmap_seed_scan(tmp_dir, scan_targets):
  try:
    os.mkdir(tmp_dir)
  except FileExistsError:
    """moving on.."""

  # Find nmap
  p = subprocess.Popen(['which', 'nmap'],
                       shell=False,
                       stdout=subprocess.PIPE)

  nmap = p.stdout.read().strip().decode("utf-8")

  # Kick off the nmap scan
  for element in scan_targets:
    ip_addr = re.match(r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', element)

    subnet = re.match(r'((?:[0-9]{1,3}\.){3}[0-9]{1,3}/\d+)', element)

    if ip_addr:
      subprocess.Popen([nmap, '-sS', '-A', element, '-Pn', '-oX', '%s/%s.nmap.xml' % (tmp_dir, element)])

    if subnet:
      subprocess.Popen([nmap, '-sS', '-A', element, '-oX' '%s/%s.nmap.xml' % (tmp_dir, element[:-3])])

  # Check to see if nmap is still running
  ps_ef = subprocess.Popen(['ps', '-ef'],
                           shell=False,
                           stdout=subprocess.PIPE)

  look_for_nmap = subprocess.Popen(['grep', 'nm\\ap'],
                                   shell=False,
                                   stdin=ps_ef.stdout,
                                   stdout=subprocess.PIPE)

  while len(look_for_nmap.communicate()[0]) is not 0:
    print('nmap is still running...')

    # Check to see if nmap is still running
    sleep(5)
    ps_ef = subprocess.Popen(['ps', '-ef'],
                             shell=False,
                             stdout=subprocess.PIPE)

    look_for_nmap = subprocess.Popen(['grep', 'nm\\ap'],
                                     shell=False,
                                     stdin=ps_ef.stdout,
                                     stdout=subprocess.PIPE)
  else:
    print('no nmap processes')
