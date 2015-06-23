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

from modules.ssh_to_core import *
from modules.send_cmd import *
from classes.db_tables import LocalNet
import modules.db_connect
import sqlalchemy
import config.seed_config as seed_info
import re
import os
import sys
import shutil

tmp_dir = '/tmp/get_base_info'
show_local_conn = tmp_dir + '/show_local_conn.txt'
show_cdp_detail = tmp_dir + '/show_cdp_detail.txt'

def get_network_info():
  shutil.rmtree(tmp_dir)
  os.mkdir(tmp_dir)
  ssh_child = cisco_enable_mode(seed_info.l_username,
                                seed_info.seed_host,
                                seed_info.l_password,
                                seed_info.l_en_password)
  if ssh_child:
    sys.stdout = open(show_local_conn, 'w')
    send_command(ssh_child, SHOW_LOCAL_CONNECTIONS)
    ssh_child.logfile_read = sys.stdout
    sys.stdout = sys.__stdout__
  if ssh_child:
    sys.stdout = open(show_cdp_detail, 'w')
    send_command(ssh_child, SHOW_CDP_DETAIL)
    ssh_child.logfile_read = sys.stdout
    ssh_child.close()
    sys.stdout = sys.__stdout__
  else:
    print('can\'t get child')
    exit()

def build_net_base():
  """Connect to the database"""
  Session = modules.db_connect.connect()
  session = Session()

  net_list = []
  with open('/tmp/get_base_info/show_local_conn.txt', 'r') as slc_f:
    data = slc_f.readlines()
    for element in data:
      m = re.search(r'((?:[0-9]{1,3}\.){3}[0-9]{1,3}/\d+)', element)
      if m:
        net_list += [m.group(0)]
  for net in net_list:
    add_net_base = LocalNet(subnet=net)
    try:
      session.add(add_net_base)
      session.commit()
    except sqlalchemy.exc.IntegrityError:
      """Then I must exist"""
      session.rollback()

def parse_cdp_detail():
  with open('sample_cdp', 'r') as sdp_f:
    data = sdp_f.readlines()
    for element in data:
      print(element)
      # regex for cdp platform: /((?<=Platform:\s)(.+?),)/
      # regex for cdp ipaddr: /((?<=IP address:\s)(?:[0-9]{1,3}\.){3}[0-9]{1,3})/
    #print(data)