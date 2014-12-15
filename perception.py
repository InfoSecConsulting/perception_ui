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
import argparse
import modules.nmap_parser
import modules.db_connect


def main():
    parser = argparse.ArgumentParser('--nmap_xml')
    parser.add_argument('--nmap_xml', dest='nmap_xml', type=str, help='What XML scan result will I scan?')

    args = parser.parse_args()
    nmap_xml = args.nmap_xml

    if nmap_xml is None:
        print('You must specify a NMAP XML file: --nmap_xml')
        return
    nmap_xml = args.nmap_xml

    clear_screen()
    try:
        check_db_connection()
    except:
        print('could not connect to the database')

    try:
        modules.nmap_parser.parse_nmap_xml(nmap_xml)
    except IsADirectoryError:
        print('I can not read an entire directory')


def clear_screen():
    os.system('clear')


def check_db_connection():
    modules.db_connect.connect_and_create_db()

if __name__ == '__main__':
    main()