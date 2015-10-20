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

import os
import argparse
import re
from lib.seed_information import get_network_info, get_hosts_to_scan, remove_inventory_hosts
from lib.ios_output_parser import local_hosts, local_connections, cdp_neighbors_detail, ios_fqdn_detail
from lib.nmap_scanner import nmap_seed_scan
from lib.nmap_output_parser import parse_seed_nmap_xml
from lib.host_profiler import profile_windows_hosts
from shutil import rmtree as rmtree

tmp_dir = '/tmp/perception'
ios_show_hosts_file = '%s/ios_show_hosts.txt' % tmp_dir
ios_show_local_conn_file = '%s/show_local_conn.txt' % tmp_dir
ios_show_cdp_detail_file = '%s/show_cdp_detail.txt' % tmp_dir
ios_show_fqdn_file = '%s/ios_show_fqdn.txt' % tmp_dir

def clear_screen():
  os.system('clear')


def main():
  parser = argparse.ArgumentParser('--seed_base,\n'
                                   '\t--seed_scan,\n'
                                   '\t--update_parse,\n'
                                   '\t--profile_windows,\n')

  parser.add_argument('--seed_base',
                      dest='seed_base',
                      action='store_true',
                      help='Use this to seed the database for networks and cdp info from the network core.')

  parser.add_argument('--seed_scan',
                      dest='seed_scan',
                      action='store_true',
                      help='Used to scan from seed_base info.')

  parser.add_argument('--update_parse',
                      dest='update_parse',
                      action='store_true',
                      help='Use this to update the database for inventory hosts with further analysis.')

  parser.add_argument('--profile_windows',
                      dest='profile_windows',
                      action='store_true',
                      help='Use this analyze Microsoft AD servers from the database.')

  args = parser.parse_args()
  seed_base = args.seed_base
  seed_scan = args.seed_scan
  update_parse = args.update_parse
  profile_windows = args.profile_windows

  clear_screen()

  if seed_base:
    get_network_info(tmp_dir,
                     ios_show_hosts_file,
                     ios_show_local_conn_file,
                     ios_show_cdp_detail_file,
                     ios_show_fqdn_file)
    # parse the local hosts file
    local_hosts(ios_show_hosts_file)

    # parse the local connections file
    local_connections(ios_show_local_conn_file)

    # parse the ios fqdn file
    ios_fqdn = ios_fqdn_detail(ios_show_fqdn_file)

    # parse the cdp detail file
    cdp_neighbors_detail(ios_show_cdp_detail_file, ios_fqdn)

    rmtree(tmp_dir)
    if seed_scan:
      print('move to scanning')
    else:
      print('done seeding')
      exit()

  if seed_scan:
    remove_inventory_hosts()
    hosts_to_scan = get_hosts_to_scan()
    nmap_seed_scan(tmp_dir, hosts_to_scan)
    for root, dirs, files in os.walk(tmp_dir):
      for name in files:
        nmap_xml = re.match(r'(^(.*?).nmap.xml)', name)
        if nmap_xml:
          parse_seed_nmap_xml(str('%s/%s' % (tmp_dir, nmap_xml.group(0))))
    rmtree(tmp_dir)

    if profile_windows:
      print('moving to Windows host profiling')
    else:
      print('done scanning hosts')
      exit()

  if profile_windows:
    print('looking for Windows hosts..')
    profile_windows_hosts()
    exit()

  if update_parse:
    print('update database')
    exit()

  else:
    clear_screen()
    print('I need arguments')
    parser.print_help()
    exit()


if __name__ == '__main__':
  try:
    main()
  except (IOError, SystemExit):
    raise
  except KeyboardInterrupt:
    print('Crtl+C Pressed. Shutting down.')
