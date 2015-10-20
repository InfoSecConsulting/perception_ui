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

from models.db_tables import LocalNet, LocalHosts, DiscoveryProtocolFindings, InventoryHost
import lib.db_connect
import sqlalchemy
from lib.ssh_to_core import *
from lib.send_cmd import *
import config.seed_config as seed_info
import os
import sys


def get_network_info(tmp_dir,
                     show_hosts_file,
                     show_local_conn_file,
                     show_cdp_detail_file,
                     ios_show_fqdn_file):
  try:
    os.mkdir(tmp_dir)
  except FileExistsError:
    """moving on.."""
  ssh_child1 = cisco_enable_mode(seed_info.l_username,
                                 seed_info.seed_host,
                                 seed_info.l_password,
                                 seed_info.l_en_password)

  ssh_child2 = cisco_enable_mode(seed_info.l_username,
                                 seed_info.seed_host,
                                 seed_info.l_password,
                                 seed_info.l_en_password)

  ssh_child3 = cisco_enable_mode(seed_info.l_username,
                                 seed_info.seed_host,
                                 seed_info.l_password,
                                 seed_info.l_en_password)

  ssh_child4 = cisco_enable_mode(seed_info.l_username,
                                 seed_info.seed_host,
                                 seed_info.l_password,
                                 seed_info.l_en_password)

  if ssh_child1:
    sys.stdout = open(show_hosts_file, 'w+')
    send_command(ssh_child1, IOSTERMLEN0)
    send_command(ssh_child1, IOS_SHOWARP)
    ssh_child1.logfile_read = sys.stdout
    ssh_child1.close()
    sys.stdout = sys.__stdout__

  if ssh_child2:
    sys.stdout = open(show_local_conn_file, 'w+')
    send_command(ssh_child2, IOSTERMLEN0)
    send_command(ssh_child2, SHOW_LOCAL_CONNECTIONS)
    ssh_child2.logfile_read = sys.stdout
    ssh_child2.close()
    sys.stdout = sys.__stdout__

  if ssh_child3:
    sys.stdout = open(show_cdp_detail_file, 'w+')
    send_command(ssh_child3, IOSTERMLEN0)
    send_command(ssh_child3, SHOW_CDP_DETAIL)
    ssh_child3.logfile_read = sys.stdout
    ssh_child3.close()
    sys.stdout = sys.__stdout__

  if ssh_child4:
    sys.stdout = open(ios_show_fqdn_file, 'w+')
    send_command(ssh_child4, IOSTERMLEN0)
    send_command(ssh_child4, IOS_SHOWHOSTNAME)
    send_command(ssh_child4, IOS_SHOWIPDOMAIN)
    ssh_child4.logfile_read = sys.stdout
    ssh_child4.close()
    sys.stdout = sys.__stdout__

  else:
    print('can\'t get child')
    exit()


def get_nets_to_scan():
  """Connect to the database"""
  Session = lib.db_connect.connect()
  session = Session()
  nets = session.query(LocalNet).all()
  nets_to_scan = []
  for l in nets:
    nets_to_scan.append(l.subnet)
  return nets_to_scan


def get_hosts_to_scan():
  """Connect to the database"""
  Session = lib.db_connect.connect()
  session = Session()
  hosts = session.query(LocalHosts).all()
  hosts_to_scan = []
  for host in hosts:
    hosts_to_scan.append(host.ip_addr)
  return hosts_to_scan

def remove_inventory_hosts():
  """Connect to the database"""
  Session = lib.db_connect.connect()
  session = Session()
  delete_stmt = sqlalchemy.delete(InventoryHost)
  session.execute(delete_stmt)
  session.commit()
