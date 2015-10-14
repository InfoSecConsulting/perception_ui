__author__ = 'arozar'


import re
from modules.db_connect import connect
from models.db_tables import InventoryHost, InventorySvc
from modules.wmic_parser import wmic_query
from sqlalchemy.sql import select
from config.seed_config import s_domain, s_password, s_username
from time import sleep

# Connect to the database
Session = connect()
session = Session()

win32_computersystem = 'select * from Win32_ComputerSystem'
win32_account = 'select * from Win32_Account'
win32_product = 'select * from Win32_Product'
win32_operatingsystem = 'select * from Win32_OperatingSystem'
win32_process = 'select * from Win32_Process'
win32_service = 'select * from Win32_Service'
win32_loggedonuser = 'select * from Win32_LoggedOnUser'
win32_logonsession = 'select * from Win32_LogonSession'
win32_useraccount = 'select * from Win32_UserAccount'


def profile_windows_hosts():
  hosts = session.query(InventoryHost).all()
  svcs = session.query(InventorySvc).all()
  windows_hosts = []

  for h_row in hosts:
    for s_row in svcs:
      host = s_row.host.ipv4_addr
      if host == h_row.ipv4_addr:
        protocol = s_row.protocol
        portid = s_row.portid
        try:
          svc_name = s_row.name
        except AttributeError:
          svc_name = 'unknown'
        try:
          svc_product = s_row.svc_product
        except AttributeError:
          svc_product = 'unknown'
        try:
          extrainfo = s_row.extrainfo
        except AttributeError:
          extrainfo = 'unknown'
        try:
          product_id = s_row.product_id
        except AttributeError:
          product_id = 'unknown'

        if svc_name == 'msrpc' or svc_name == 'ldap' or svc_name == 'globalcatLDAPssl':
          # print('\t %s | %s | %s | %s | %s | %s' % (protocol, portid, svc_name, svc_product, extrainfo, product_id))
          # print('\n')
          windows_hosts.append(h_row.ipv4_addr)
  win_host_set = set(windows_hosts)
  print(win_host_set)

  #for h in hosts:
  #  for s in svcs:
  #    if s.host.ipv4_addr == h.ipv4_addr:

  #      # Look for Windows AD server
  #      if s.protocol == 'tcp' and s.portid == 3269 and s.name == 'globalcatLDAPssl' \
  #        or s.portid == 3269 and s.name == 'ldap':  # Possibly found AD server!
  #        print('%s may be an Active Directory Server' % s.host.ipv4_addr)
  #        cs_query = wmic_query(s_domain, s_username, s_password, s.host.ipv4_addr, win32_computersystem)
  #        failed_login = re.search(r'(failed NT status)', str(cs_query))
  #        error_login = re.search(r'(ERROR: Login to remote object)', str(cs_query))
  #        if failed_login:
  #          print('credentials are wrong or %s is not a Windows host' % s.host.ipv4_addr)
  #          print('\n')
  #        elif error_login:
  #          print('error logging in, possible timeout..')
  #          print('\n')

  #        else:
  #          os_query = wmic_query(s_domain, s_username, s_password, s.host.ipv4_addr, win32_operatingsystem)

  #          print('Hostname: %s' % cs_query['DNSHostName'])
  #          print('Primary Owner: %s' % cs_query['PrimaryOwnerName'])
  #          print('Manufacturer: %s' % cs_query['Manufacturer'])
  #          print('Number of Logical Processors: %s' % cs_query['NumberOfLogicalProcessors'])
  #          print('System Type: %s' % cs_query['SystemType'])
  #          print('\n')
  #          print('OS Name: %s' % os_query['Name'])
  #          print('Version: %s' % os_query['Version'])
  #          print('OS Type: %s' % os_query['OSType'])
  #          print('OS Build Number: %s' % os_query['BuildNumber'])
  #          print('CSD Version: %s' % os_query['CSDVersion'])
  #          print('Service Pack Minor Version: %s' % os_query['ServicePackMinorVersion'])
  #          print('OS Product Suite: %s' % os_query['OSProductSuite'])
  #          print('OS Architecture: %s' % os_query['OSArchitecture'])
  #          print('OS SKU: %s' % os_query['OperatingSystemSKU'])
  #          print('Data Execution Prevention for 32Bit Applications: %s' % os_query['DataExecutionPrevention_32BitApplications'])
  #          print('Data Execution Prevention Support Policy: %s' % os_query['DataExecutionPrevention_SupportPolicy'])
  #          print('\n')

  #      # Look for standard Windows device
  #      if s.protocol == 'tcp' and s.portid == 445 and s.name == 'microsoft-ds':  # Possibly found a Windows device!
  #        print('%s may be a Windows device' % s.host.ipv4_addr)
  #        cs_query = wmic_query(s_domain, s_username, s_password, s.host.ipv4_addr, win32_computersystem)
  #        failed_login = re.search(r'(failed NT status)', str(cs_query))
  #        error_login = re.search(r'(ERROR: Login to remote object)', str(cs_query))
  #        host_is_ad = re.search(r'(Domain_Controller)', str(cs_query))
  #        if failed_login:
  #          print('credentials are wrong or %s is not a Windows host' % s.host.ipv4_addr)
  #          print('\n')
  #        elif error_login:
  #          print('error logging in, possible timeout..')
  #          print('\n')
  #        elif host_is_ad:
  #          print('wait to query this host..')
  #          print('\n')
  #        else:
  #          os_query = wmic_query(s_domain, s_username, s_password, s.host.ipv4_addr, win32_operatingsystem)

  #          print('Hostname: %s' % cs_query['DNSHostName'])
  #          print('Primary Owner: %s' % cs_query['PrimaryOwnerName'])
  #          print('Manufacturer: %s' % cs_query['Manufacturer'])
  #          print('Number of Logical Processors: %s' % cs_query['NumberOfLogicalProcessors'])
  #          print('System Type: %s' % cs_query['SystemType'])
  #          print('\n')
  #          print('OS Name: %s' % os_query['Name'])
  #          print('Version: %s' % os_query['Version'])
  #          print('OS Type: %s' % os_query['OSType'])
  #          print('OS Build Number: %s' % os_query['BuildNumber'])
  #          print('CSD Version: %s' % os_query['CSDVersion'])
  #          print('Service Pack Minor Version: %s' % os_query['ServicePackMinorVersion'])
  #          print('OS Product Suite: %s' % os_query['OSProductSuite'])
  #          print('OS Architecture: %s' % os_query['OSArchitecture'])
  #          print('OS SKU: %s' % os_query['OperatingSystemSKU'])
  #          print('Data Execution Prevention for 32Bit Applications: %s' % os_query['DataExecutionPrevention_32BitApplications'])
  #          print('Data Execution Prevention Support Policy: %s' % os_query['DataExecutionPrevention_SupportPolicy'])
  #          print('\n')
