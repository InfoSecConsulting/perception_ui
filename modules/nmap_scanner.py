#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
(C) Copyright [2014] InfoSec Consulting, Inc.

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
import modules.nmap_scans

try:
    import nmap

except:
    ImportError
    print('Installing Python Nmap..')
    os.system('cd packages/python-nmap-0.3.4/ && python3 setup.py install')
    import nmap

import argparse


def main():
    parser = argparse.ArgumentParser('usage%prog ' +
                                     '--host_file < --host_file=hosts.txt >')
    parser.add_argument('--host_file', dest='dst_hosts', type=file, help='specify a target host file')

    args = parser.parse_args()
    dst_hosts = args.dst_hosts

    if dst_hosts is None:
        print('I need to know what host[s] to scan')
        print(parser.usage)
        exit(0)
    else:
        for line in dst_hosts:
            dst_host = line.rstrip()
            nmscan = nmap.PortScanner()
            nmscan.scan(dst_host, arguments='-sS -A -v')
            for host in nmscan.all_hosts():
                print('---------------------------')
                print('Host : %s (%s)' % (host, nmscan[host].hostname()))
                print('State : %s' % nmscan[host].state())

                for protocol in nmscan[host].all_protocols():
                    print('---------------------------')
                    print('Protocol : %s' % protocol)

                    lport = list(nmscan[host][protocol].keys())
                    lport.sort()
                    for port in lport:
                        print('port : %s\tstate : %s' % (port, nmscan[host][protocol][port]['state']))


if __name__ == '__main__':
    main()