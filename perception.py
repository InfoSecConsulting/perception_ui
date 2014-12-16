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
import modules.nmap_seed_parser
import modules.db_connect
import modules.export_xlsx


def main():
    parser = argparse.ArgumentParser('--nmap_xml, , --seed_parse, --xlsx_export, --drop_all')
    parser.add_argument('--nmap_xml', dest='nmap_xml', type=str, help='What XML scan results should I parse?')
    parser.add_argument('--seed_parse', dest='seed_parse', action='store_true',
                        help='Use this io seed the database for inventory, if deeper analysis was already done on '
                        'these hosts, do not use this switch. It will destroy all services and re-parse.')
    parser.add_argument('--xlsx_export', dest='xlsx_export', action='store_true',
                        help='Export to XLSX after parsing.')
    parser.add_argument('--drop_all', dest='drop_all', action='store_true',
                        help='Drop all the tables from the database.')

    args = parser.parse_args()
    nmap_xml = args.nmap_xml
    seed_parse = args.seed_parse
    xlsx_export = args.xlsx_export
    drop_all = args.drop_all

    if drop_all:
        clear_screen()
        if input('Are you sure?: ') == 'yes':
            modules.db_connect.connect_and_drop_all()
            clear_screen()
            print('Dropped all tables.')
            exit()

    #if nmap_xml is None:
    #    print('You must specify a NMAP XML file: --nmap_xml')
    #    return

    clear_screen()

    try:
        modules.db_connect.connect_and_create_db()
    except:
        print('could not connect to the database')

    if seed_parse:
        try:
            modules.nmap_seed_parser.parse_nmap_xml(nmap_xml)
        except IsADirectoryError:
            print('I can not read an entire directory')

    if xlsx_export:
        clear_screen()
        print('Generating report..')
        modules.export_xlsx.reporter()
        clear_screen()
        print('Done.')
        exit()

    else:
        clear_screen()
        print('Done.')


def clear_screen():
    os.system('clear')

if __name__ == '__main__':
    main()