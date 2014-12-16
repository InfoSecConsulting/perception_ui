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
import sys
import modules.db_connect
from classes.db_tables import InventoryHost

try:
    import xlsxwriter
except ImportError:
    print('Installing XlsxWriter..')
    os.system('cd packages/XlsxWriter-0.6.3/ && python3 setup.py install')
    import xlsxwriter


def reporter():

    """Connect to the database"""
    global host_name, ipv4_addr, ipv6_addr, macaddr, host_type
    Session = modules.db_connect.connect()
    session = Session()
    report = xlsxwriter.Workbook('perception_report.xlsx')
    top_row_format = report.add_format({'bold': True})
    top_row_format.set_border(style=1)
    top_row_format.set_bg_color('#B8B8B8')

    host_row_format = report.add_format()
    host_row_format.set_border(style=1)
    host_row_format.set_bg_color('#CCCCCC')

    host_nse_output_top_format = report.add_format({'bold': True})
    host_nse_output_top_format.set_border(style=1)
    host_nse_output_top_format.set_bg_color('#B8B8B8')
    #host_nse_output_top_format.merge_range('C5:I5')

    host_nse_output_format = report.add_format()
    host_nse_output_format.set_border(style=1)
    host_nse_output_format.set_bg_color('#CCCCCC')
    #host_nse_output_format.merge_range('C5:I5')

    """Build the host_overview_worksheet"""
    host_overview_worksheet = report.add_worksheet()

    """Build the host_detail_worksheet"""
    host_detail_worksheet = report.add_worksheet()

    """Size up the worksheets"""
    host_overview_worksheet.set_column('B:B', 24)
    host_overview_worksheet.set_column('C:C', 15)
    host_overview_worksheet.set_column('D:D', 15)
    host_overview_worksheet.set_column('E:E', 15)
    host_overview_worksheet.set_column('F:F', 15)
    host_overview_worksheet.set_column('G:G', 20)
    host_overview_worksheet.set_column('H:H', 15)

    host_detail_worksheet.set_column('B:B', 38)
    host_detail_worksheet.set_column('C:C', 16)
    host_detail_worksheet.set_column('D:D', 16)
    host_detail_worksheet.set_column('E:E', 28)
    host_detail_worksheet.set_column('F:F', 15)
    host_detail_worksheet.set_column('H:G', 20)
    host_detail_worksheet.set_column('H:H', 25)
    host_detail_worksheet.set_column('I:I', 10)

    # Add a bold format to use to highlight cells.

    # Write some simple text.
    host_overview_worksheet.write('B2', 'Hostname', top_row_format)
    host_overview_worksheet.write('C2', 'IP v4 Address', top_row_format)
    host_overview_worksheet.write('D2', 'IP v6 Address', top_row_format)
    host_overview_worksheet.write('E2', 'MAC Address', top_row_format)
    host_overview_worksheet.write('F2', 'MAC Vendor', top_row_format)
    host_overview_worksheet.write('G2', 'Operating System', top_row_format)
    host_overview_worksheet.write('H2', 'Host Type', top_row_format)

    host_detail_worksheet.write('B2', 'Hostname', top_row_format)
    host_detail_worksheet.write('C2', 'IP v4 Address', top_row_format)
    host_detail_worksheet.write('D2', 'IP v6 Address', top_row_format)
    host_detail_worksheet.write('E2', 'MAC Address', top_row_format)
    host_detail_worksheet.write('F2', 'MAC Vendor', top_row_format)
    host_detail_worksheet.write('G2', 'Host Type', top_row_format)
    host_detail_worksheet.write('H2', 'Operating System', top_row_format)
    host_detail_worksheet.write('I2', 'Version', top_row_format)

    #host_detail_worksheet.write('A1', 'Hello')
    inventory_hosts = session.query(InventoryHost).all()
    overview_row = 2
    overview_col = 1
    for host in inventory_hosts:
        host_overview_worksheet.write(overview_row, overview_col, host.host_name, host_row_format)
        host_overview_worksheet.write(overview_row, overview_col + 1, host.ipv4_addr, host_row_format)
        host_overview_worksheet.write(overview_row, overview_col + 2,  host.ipv6_addr, host_row_format)
        host_overview_worksheet.write(overview_row, overview_col + 3, host.macaddr, host_row_format)
        host_overview_worksheet.write(overview_row, overview_col + 4, host.mac_vendor.name, host_row_format)
        host_overview_worksheet.write(overview_row, overview_col + 5, host.product.name, host_row_format)
        host_overview_worksheet.write(overview_row, overview_col + 6, host.host_type, host_row_format)
        overview_row += 1

    detail_row = 2
    detail_col = 1
    for host in inventory_hosts:
        host_detail_worksheet.write(detail_row, detail_col, host.host_name, host_row_format)
        host_detail_worksheet.write(detail_row, detail_col + 1, host.ipv4_addr, host_row_format)
        host_detail_worksheet.write(detail_row, detail_col + 2,  host.ipv6_addr, host_row_format)
        host_detail_worksheet.write(detail_row, detail_col + 3, host.macaddr, host_row_format)
        host_detail_worksheet.write(detail_row, detail_col + 4, host.mac_vendor.name, host_row_format)
        host_detail_worksheet.write(detail_row, detail_col + 5, host.host_type, host_row_format)
        host_detail_worksheet.write(detail_row, detail_col + 6, host.product.name, host_row_format)
        host_detail_worksheet.write(detail_row, detail_col + 7, host.product.version, host_row_format)
        detail_row += 1

        for scripts in host.host_nse_scripts:
            detail_row += 1
            host_detail_worksheet.write(detail_row, detail_col, 'Host NSE Script Name', top_row_format)
            host_detail_worksheet.merge_range(detail_row, detail_col + 1, detail_row, detail_col + 7,
                                              'Output', top_row_format)
            detail_row += 1
            host_detail_worksheet.write(detail_row, detail_col, scripts.name, host_row_format)
            host_detail_worksheet.merge_range(detail_row, detail_col + 1, detail_row, detail_col + 7,
                                              scripts.output, host_row_format)

            detail_row += 1

            for ports in host.inventory_svcs:
                detail_row += 1
                host_detail_worksheet.write(detail_row, detail_col, 'Protocol', top_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 1, 'Port', top_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 2, 'Name', top_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 3, 'Svc Product', top_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 4, 'Extra Info', top_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 5, 'Product', top_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 6, 'Version', top_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 7, 'Update', top_row_format)
                detail_row += 1
                host_detail_worksheet.write(detail_row, detail_col, ports.protocol, host_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 1, ports.portid, host_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 2, ports.name, host_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 3, ports.svc_product, host_row_format)
                host_detail_worksheet.write(detail_row, detail_col + 4, ports.extra_info, host_row_format)
                try:
                    host_detail_worksheet.write(detail_row, detail_col + 5, ports.product.name, host_row_format)
                    host_detail_worksheet.write(detail_row, detail_col + 6, ports.product.version, host_row_format)
                    host_detail_worksheet.write(detail_row, detail_col + 7, ports.product.product_update,
                                                host_row_format)
                except AttributeError:
                    host_detail_worksheet.write(detail_row, detail_col + 5, 'unknown', host_row_format)
                    host_detail_worksheet.write(detail_row, detail_col + 6, 'unknown', host_row_format)
                    host_detail_worksheet.write(detail_row, detail_col + 7, 'unknown', host_row_format)

            detail_row += 1

    # Insert an image.
    #worksheet.insert_image('B5', 'logo.png')

    report.close()
    session.close()