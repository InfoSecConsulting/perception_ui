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

from models.db_tables import LocalNet, DiscoveryProtocolFindings, InventoryHost, LocalHosts
from sqlalchemy import update, delete
import lib.db_connect
import sqlalchemy
import re

def local_hosts(show_hosts_file):
  """Connect to the database"""
  Session = lib.db_connect.connect()
  session = Session()

  host_dict_list = []
  with open(show_hosts_file, 'r') as shosts_f:
    # clean up the old local connections
    session.query(LocalHosts).filter().delete()
    session.commit()

    hosts_data = shosts_f.readlines()
    for element in hosts_data:
      ip_addrs = re.search(r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                           r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                           r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                           r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', element)

      mac_addrs = re.search(r'(([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4})', element)
      try:
        host_dict = {'ip_addr': ip_addrs.group(0), 'mac_addr': mac_addrs.group(0)}
        host_dict_list.append(host_dict)
      except AttributeError:
        """Likely NoneType"""
  for host in host_dict_list:
    add_host = LocalHosts(ip_addr=host['ip_addr'],
                          mac_addr=host['mac_addr'])
    try:
      session.add(add_host)
      session.commit()
    except sqlalchemy.exc.IntegrityError:
      """Then I must exist"""
      session.rollback()
  shosts_f.close()

def local_connections(show_local_conn_file):
  """Connect to the database"""
  Session = lib.db_connect.connect()
  session = Session()

  net_list = []
  with open(show_local_conn_file, 'r') as slc_f:
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
  slc_f.close()


def ios_fqdn_detail(ios_show_fqdn_file):
  fqdn = []
  with open(ios_show_fqdn_file, 'r') as sfqdn_f:
    fqdn_data = sfqdn_f.readlines()
    for element in fqdn_data:
      reg_ip_domain_name = re.search(r'(ip domain-name\s+.+?)\n', element)
      reg_hostname = re.search(r'(hostname\s+.+?)\n', element)
      if reg_hostname:
        fqdn += reg_hostname.group(0).split(' ')[1].strip() + '.'
      if reg_ip_domain_name:
        fqdn += reg_ip_domain_name.group(0).split(' ')[2].strip()
  ios_fqdn = ''.join(fqdn)
  return ios_fqdn


def cdp_neighbors_detail(show_cdp_detail_file, ios_fqdn):
  """Connect to the database"""
  Session = lib.db_connect.connect()
  session = Session()

  """Clean up the current CDP info"""
  delete_stmt = (delete(DiscoveryProtocolFindings,
                            whereclause=DiscoveryProtocolFindings.local_device_id == ios_fqdn))
  session.execute(delete_stmt)
  session.commit()

  with open(show_cdp_detail_file, 'r') as scdp_f:
    data = scdp_f.read()
    data_list = str(data).split('-------------------------')
    for element in data_list:
      discovery_list = []
      reg_device_id = re.search(r'(Device ID:.+?)\n', element)
      try:
        discovery_list += [re.sub(r':\s+', ':', reg_device_id.group(0).strip())]
      except AttributeError:
        discovery_list.append('Device ID:')
      reg_entry_addrs = re.search(r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                                  r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                                  r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                                  r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', element)
      try:
        discovery_list.append('IP:%s' % str(reg_entry_addrs.group(0).strip('\n')))
      except AttributeError:
        discovery_list.append('IP:')
      reg_platform = re.search(r'(Platform:.+?)\n', element)
      try:
        platform_line = re.sub(r':\s+', ':', reg_platform.group(0).strip())
        platform_capabilities = platform_line.split(',  ')
        discovery_list.append(platform_capabilities[0])
        discovery_list.append(platform_capabilities[1])
      except AttributeError:
        discovery_list.append('Platform:')
        discovery_list.append('Capabilities:')
      reg_int = re.search(r'(Interface:.+?)\n', element)
      try:
        int_line = re.sub(r':\s+', ':', reg_int.group(0).strip())
        interface_port_id = int_line.split(',  ')
        discovery_list.append(interface_port_id[0])
        discovery_list.append(interface_port_id[1])
      except AttributeError:
        discovery_list.append('Interface:')
        discovery_list.append('Port ID (outgoing port):')
      reg_advertisment_ver = re.search(r'(advertisement version:.+?)\n', element)
      try:
        discovery_list += [re.sub(r':\s+', ':', reg_advertisment_ver.group(0).strip())]
      except AttributeError:
        discovery_list.append('advertisement version:')
      reg_protocol_hello = re.search(r'(Protocol Hello:.+?)\n', element)
      try:
        discovery_list += [re.sub(r':\s+', ':', reg_protocol_hello.group(0).strip())]
      except AttributeError:
        discovery_list.append('Protocol Hello:')
      reg_vtp_mgnt = re.search(r'(VTP Management Domain:.+?)\n', element)
      try:
        discovery_list += [re.sub(r':\s+', ':', reg_vtp_mgnt.group(0).strip())]
      except AttributeError:
        discovery_list.append('VTP Management Domain:')
      reg_native_vlan = re.search(r'(Native VLAN:.+?)\n', element)
      try:
        discovery_list += [re.sub(r':\s+', ':', reg_native_vlan.group(0).strip())]
      except AttributeError:
        discovery_list.append('Native VLAN:')
      reg_duplex = re.search(r'(Duplex:.+?)\n', element)
      try:
        discovery_list += [re.sub(r':\s+', ':', reg_duplex.group(0).strip())]
      except AttributeError:
        discovery_list.append('Duplex:')
      reg_power_drawn = re.search(r'(Power drawn:.+?)\n', element)
      try:
        discovery_list += [re.sub(r':\s+', ':', reg_power_drawn.group(0).strip())]
      except AttributeError:
        discovery_list.append('Power drawn:')

      discovery_dictionary = dict(map(str, x.split(':')) for x in discovery_list)

      for k, v in discovery_dictionary.items():
        if v is '':
          discovery_dictionary[k] = None

      if discovery_dictionary['Device ID'] is not None:
        add_cdp_data = DiscoveryProtocolFindings(local_device_id=ios_fqdn,
                                                 remote_device_id=discovery_dictionary['Device ID'],
                                                 ip_addr=discovery_dictionary['IP'],
                                                 platform=discovery_dictionary['Platform'],
                                                 capabilities=discovery_dictionary['Capabilities'],
                                                 interface=discovery_dictionary['Interface'],
                                                 port_id=discovery_dictionary['Port ID (outgoing port)'],
                                                 discovery_version=discovery_dictionary['advertisement version'],
                                                 protocol_hello=discovery_dictionary['Protocol Hello'],
                                                 vtp_domain = discovery_dictionary['VTP Management Domain'],
                                                 native_vlan=discovery_dictionary['Native VLAN'],
                                                 duplex=discovery_dictionary['Duplex'],
                                                 power_draw=discovery_dictionary['Power drawn'])
        session.add(add_cdp_data)
        session.commit()
  scdp_f.close()
