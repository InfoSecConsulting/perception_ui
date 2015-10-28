import sys
from os import mkdir
from flask.ext.sqlalchemy import SQLAlchemy
from app import db
from app.main.models import LocalNet, LocalHosts, InventoryHost, CoreRouters, LinuxUser
#from app import create_app
from app.lib.ssh_to_core import *
from app.lib.send_cmd import send_command
from app.lib.cisco_cmds import IOSTERMLEN0,\
  IOS_SHOWARP,\
  SHOW_LOCAL_CONNECTIONS, \
  SHOW_CDP_DETAIL,\
  IOS_SHOWHOSTNAME,\
  IOS_SHOWIPDOMAIN
from app.lib.crypt import decrypt_string

#app = create_app('default')
#db = SQLAlchemy(app)
#db.init_app(app)

# get core router user service account info
core_router = CoreRouters.query.first()
ip_addr = core_router.ip_addr
username = core_router.linux_users.username
password = decrypt_string(str.encode(core_router.linux_users.encrypted_password),
                          str.encode(core_router.linux_users.encrypted_password_salt))
enable_password = decrypt_string(str.encode(core_router.linux_users.encrypted_enable_password), str.encode(core_router.linux_users.encrypted_enable_password_salt))

def get_network_info(tmp_dir,
                     show_hosts_file,
                     show_local_conn_file,
                     show_cdp_detail_file,
                     ios_show_fqdn_file):
  try:
    mkdir(tmp_dir)
  except FileExistsError:
    """moving on.."""
  ssh_child1 = cisco_enable_mode(username,
                                 ip_addr,
                                 password.decode("utf-8"),
                                 enable_password.decode("utf-8"))

  ssh_child2 = cisco_enable_mode(username,
                                 ip_addr,
                                 password.decode("utf-8"),
                                 enable_password.decode("utf-8"))

  ssh_child3 = cisco_enable_mode(username,
                                 ip_addr,
                                 password.decode("utf-8"),
                                 enable_password.decode("utf-8"))

  ssh_child4 = cisco_enable_mode(username,
                                 ip_addr,
                                 password.decode("utf-8"),
                                 enable_password.decode("utf-8"))

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
  nets = db.session.query(LocalNet).all()
  nets_to_scan = []
  for l in nets:
    nets_to_scan.append(l.subnet)
  return nets_to_scan


def get_hosts_to_scan():
  hosts = db.session.query(LocalHosts).all()
  hosts_to_scan = []
  for host in hosts:
    hosts_to_scan.append(host.ip_addr)
  return hosts_to_scan


def remove_inventory_hosts():
  delete_stmt = db.delete(InventoryHost)
  db.session.execute(delete_stmt)
  db.session.commit()
