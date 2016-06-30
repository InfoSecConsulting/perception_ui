from app import db
from sqlalchemy.dialects import postgresql
from app.lib.crypt import encrypt_string

import datetime


def _get_date():
    return datetime.datetime.now()


class Base(db.Model):
  __abstract__ = True

  created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
  updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Vendor(db.Model):
  __tablename__ = 'vendors'

  id = db.Column(db.Integer, db.Sequence('vendors_id_seq'), primary_key=True, nullable=False)
  name = db.Column(db.Text, unique=True, nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class Product(db.Model):
  __tablename__ = 'products'

  id = db.Column(db.Integer, db.Sequence('products_id_seq'), primary_key=True, nullable=False)

  product_type = db.Column(db.Text, nullable=False)

  """Relation to tie vendors to products"""
  vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
  vendor = db.relationship('Vendor', backref='products', order_by=id)

  name = db.Column(db.Text, nullable=False)
  version = db.Column(db.Text)
  product_update = db.Column(db.Text)
  edition = db.Column(db.Text)
  language = db.Column(db.Text)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class OpenvasAdmin(db.Model):
  __tablename__ = 'openvas_admin'

  id = db.Column(db.Integer, db.Sequence('openvas_admin_id_seq'), primary_key=True, nullable=False)
  username = db.Column(db.Text, unique=True, nullable=False)
  password = db.Column(postgresql.UUID, nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class MACVendor(db.Model):
  __tablename__ = 'mac_vendors'

  id = db.Column(db.Integer, db.Sequence('mac_vendors_id_seq'), primary_key=True, nullable=False)
  name = db.Column(db.Text, unique=True)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class SmbUser(db.Model):
  __tablename__ = 'smb_users'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  username = db.Column(db.String, nullable=False, unique=True)
  openvas_lsc_id = db.Column(postgresql.UUID)
  encrypted_password = db.Column(db.String, nullable=False)
  encrypted_password_salt = db.Column(db.String, nullable=False)
  domain_name = db.Column(db.String, nullable=False)
  description = db.Column(db.String)

  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)

  def __init__(self,
               username=None,
               password=None,
               domain_name=None,
               description=None,
               openvas_lsc_id=None):

    if domain_name:
      self.domain_name = domain_name

    if description:
      self.description = description

    if username:
      self.username = username

    if password:
      password_tup = encrypt_string(str.encode(password))
      self.encrypted_password = password_tup[0].decode("utf-8")
      self.encrypted_password_salt = password_tup[1].decode("utf-8")

    if openvas_lsc_id:
      self.openvas_lsc_id = openvas_lsc_id

class LinuxUser(db.Model):
  __tablename__ = 'linux_users'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  username = db.Column(db.String, nullable=False, unique=True)
  openvas_lsc_id = db.Column(postgresql.UUID)
  encrypted_password = db.Column(db.String, nullable=False)
  encrypted_password_salt = db.Column(db.String, nullable=False)
  encrypted_enable_password = db.Column(db.String)
  encrypted_enable_password_salt = db.Column(db.String)
  description = db.Column(db.String)

  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)

  def __init__(self,
               username=None,
               password=None,
               enable_password=None,
               description=None,
               openvas_lsc_id=None):
    if description:
      self.description = description

    if username:
      self.username = username

    if password:
      password_tup = encrypt_string(str.encode(password))
      self.encrypted_password = password_tup[0].decode("utf-8")
      self.encrypted_password_salt = password_tup[1].decode("utf-8")

    if enable_password:
      enable_password_tup = encrypt_string(str.encode(enable_password))
      self.encrypted_enable_password = enable_password_tup[0].decode('utf-8')
      self.encrypted_enable_password_salt = enable_password_tup[1].decode('utf-8')

    if openvas_lsc_id:
      self.openvas_lsc_id = openvas_lsc_id


class InventoryHost(db.Model):
  __tablename__ = 'inventory_hosts'

  id = db.Column(db.Integer, db.Sequence('inventory_hosts_id_seq'), primary_key=True, nullable=False)
  ipv4_addr = db.Column(postgresql.INET, unique=True)
  ipv6_addr = db.Column(postgresql.INET)
  macaddr = db.Column(postgresql.MACADDR)
  host_type = db.Column(db.Text)

  """Relation to tie mac address vendors to inventory hosts"""
  mac_vendor_id = db.Column(db.Integer, db.ForeignKey('mac_vendors.id'))
  mac_vendor = db.relationship('MACVendor', backref='inventory_hosts', order_by=id)

  state = db.Column(db.Text)
  host_name = db.Column(db.Text)

  """Relation to tie an OS inventory hosts"""
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
  product = db.relationship('Product', backref='inventory_hosts', order_by=id)

  arch = db.Column(db.Text)

  """Relation to tie users to inventory hosts"""
  smb_user_id = db.Column(db.Integer, db.ForeignKey('smb_users.id'))
  smb_user = db.relationship('SmbUser', backref='inventory_hosts', order_by=id)

  linux_user_id = db.Column(db.Integer, db.ForeignKey('linux_users.id'))
  linux_user = db.relationship('LinuxUser', backref='inventory_hosts', order_by=id)

  info = db.Column(db.Text)
  comments = db.Column(db.Text)
  bad_ssh_key = db.Column(db.Boolean)
  last_openvas_scan = db.Column(db.TIMESTAMP(timezone=False))
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class HostNseScript(db.Model):
  __tablename__ = 'host_nse_scripts'

  id = db.Column(db.Integer, db.Sequence('host_nse_scripts_id_seq'), primary_key=True, nullable=False)

  """Relation to host"""
  inventory_host_id = db.Column(db.Integer, db.ForeignKey('inventory_hosts.id', ondelete='cascade'))
  inventory_host = db.relationship('InventoryHost', backref='host_nse_scripts', order_by=id)

  name = db.Column(db.Text, nullable=False)
  output = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class InventorySvc(db.Model):
  __tablename__ = 'inventory_svcs'

  id = db.Column(db.Integer, db.Sequence('inventory_svcs_id_seq'), primary_key=True, nullable=False)

  """Relation to inventory inventory_host"""
  inventory_host_id = db.Column(db.Integer, db.ForeignKey('inventory_hosts.id', ondelete='cascade'))
  inventory_host = db.relationship('InventoryHost', backref='inventory_svcs', order_by=id)

  protocol = db.Column(db.Text)
  portid = db.Column(db.Integer)
  name = db.Column(db.Text)
  svc_product = db.Column(db.Text)
  extra_info = db.Column(db.Text)

  """Relation to tie products to inventory services"""
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
  product = db.relationship('Product', backref='inventory_svcs', order_by=id)

  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class SvcNseScript(db.Model):
  __tablename__ = 'svc_nse_scripts'

  id = db.Column(db.Integer, db.Sequence('svc_nse_scripts_id_seq'), primary_key=True, nullable=False)

  """Relation to inventory_svc"""
  inventory_svc_id = db.Column(db.Integer, db.ForeignKey('inventory_svcs.id', ondelete='cascade'))
  inventory_svc = db.relationship('InventorySvc', backref='svc_nse_scripts', order_by=id)

  name = db.Column(db.Text, nullable=False)
  output = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class LocalNet(db.Model):
  __tablename__ = 'local_nets'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  subnet = db.Column(postgresql.CIDR, unique=True)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class DiscoveryProtocolFinding(db.Model):
  __tablename__ = 'discovery_protocol_findings'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  local_device_id = db.Column(db.Text, nullable=False)
  remote_device_id = db.Column(db.Text, nullable=False)
  ip_addr = db.Column(postgresql.INET)
  platform = db.Column(db.Text)
  capabilities = db.Column(db.Text)
  interface = db.Column(db.Text)
  port_id = db.Column(db.Text)
  discovery_version = db.Column(db.Integer)
  protocol_hello = db.Column(db.Text)
  vtp_domain = db.Column(db.Text)
  native_vlan = db.Column(db.Integer)
  duplex = db.Column(db.Text)
  power_draw = db.Column(db.Text)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class LocalHost(db.Model):
  __tablename__ = 'local_hosts'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  ip_addr = db.Column(postgresql.INET, unique=True, nullable=False)
  mac_addr = db.Column(postgresql.MACADDR, unique=True, nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class CoreRouter(Base):
  __tablename__ = 'core_routers'

  id = db.Column(db.Integer, db.Sequence('core_routers_id_seq'), primary_key=True, nullable=False)
  ip_addr = db.Column(postgresql.INET, unique=True, nullable=False)
  host_name = db.Column(db.Text, unique=True)

  """Relation to linux_user"""
  linux_user_id = db.Column(db.Integer, db.ForeignKey('linux_users.id', ondelete='cascade'))
  linux_users = db.relationship('LinuxUser', backref='core_routers', order_by=id)

  def __init__(self, linux_user_id,
               ip_addr,
               host_name=None):

    self.linux_user_id = linux_user_id
    self.ip_addr = ip_addr

    if host_name:
      self.host_name = host_name


class SnmpString(Base):
  __tablename__ = 'snmp_strings'

  id = db.Column(db.Integer, db.Sequence('snmp_strings_id_seq'), primary_key=True, nullable=False)
  community_string_encrypted = db.Column(db.String)
  community_string_encrypted_salt = db.Column(db.String)
  snmp_user_encrypted = db.Column(db.String)
  snmp_user_encrypted_salt = db.Column(db.String)
  snmp_group_encrypted = db.Column(db.String)
  snmp_group_encrypted_salt = db.Column(db.String)

  def __init__(self,
               community_string=None,
               snmp_user=None,
               snmp_group=None):

    if community_string:
      community_string_tup = encrypt_string(str.encode(community_string))
      self.community_string_encrypted = community_string_tup[0].decode("utf-8")
      self.community_string_encrypted_salt = community_string_tup[1].decode("utf-8")

    if snmp_user:
      snmp_user_tup = encrypt_string(str.encode(snmp_user))
      self.snmp_user_encrypted = snmp_user_tup[0].decode('utf-8')
      self.snmp_user_encrypted_salt = snmp_user_tup[1].decode('utf-8')

    if snmp_group:
      snmp_group_tup = encrypt_string(str.encode(snmp_group))
      self.snmp_group_encrypted = snmp_group_tup[0].decode('utf-8')
      self.snmp_group_encrypted_salt = snmp_group_tup[1].decode('utf-8')


class OpenvasLastUpdate(db.Model):
  __tablename__ = 'openvas_last_updates'

  id = db.Column(db.Integer, db.Sequence('openvas_last_updates_id_seq'), primary_key=True, nullable=False)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), nullable=False)


class Target(db.Model):
  __tablename__ = 'targets'

  id = db.Column(db.Integer, db.Sequence('targets_id_seq'), primary_key=True, nullable=False)
  ip_addr = db.Column(postgresql.INET, unique=True)
  subnet = db.Column(postgresql.CIDR, unique=True)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)

  def __init__(self,
               ipd_addr=None,
               subnet=None):

    if ipd_addr:
      self.ip_addr = ipd_addr

    if subnet:
      self.subnet = subnet


class DayOfTheWeek(db.Model):
  __tablename__ = 'days_of_the_week'

  id = db.Column(db.Integer, db.Sequence('days_of_the_week_id_seq'), primary_key=True, nullable=False)
  name = db.Column(db.Text, nullable=False, unique=True)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)


class ScheduleType(db.Model):
  __tablename__ = 'schedule_types'

  id = db.Column(db.Integer, db.Sequence('schedule_types_id_seq'), primary_key=True, nullable=False)
  name = db.Column(db.Text, nullable=False, unique=True)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)


class Schedule(db.Model):
  __tablename__ = 'schedules'

  id = db.Column(db.Integer, db.Sequence('schedules_id_seq'), primary_key=True, nullable=False)
  name = db.Column(db.Text, nullable=False)

  """Relation to schedule_types"""
  schedule_type_id = db.Column(db.Integer, db.ForeignKey('schedule_types.id'))
  schedule_types = db.relationship('ScheduleType', backref='schedules', order_by=id)

  dynamic = db.Column(db.BOOLEAN)

  start_date = db.Column(db.TIMESTAMP(timezone=False))
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class DailySchedule(db.Model):
  __tablename__ = 'daily_schedules'

  id = db.Column(db.Integer, db.Sequence('daily_schedules_id_seq'), primary_key=True, nullable=False)

  """Relation to schedules"""
  schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
  schedules = db.relationship('Schedule', backref='daily_schedules', order_by=id)

  """Relation to days_of_week"""
  day_of_week_id = db.Column(db.Integer, db.ForeignKey('days_of_the_week.id'), nullable=False)
  days_of_week = db.relationship('DayOfTheWeek', backref='daily_schedules', order_by=id)

  time_of_day = db.Column(db.TIME, nullable=False)
  start_date = db.Column(db.TIMESTAMP(timezone=False), nullable=False)
  end_date = db.Column(db.TIMESTAMP(timezone=False))
  recurrence = db.Column(db.Integer, nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class WeeklySchedule(db.Model):
  __tablename__ = 'weekly_schedules'

  id = db.Column(db.Integer, db.Sequence('daily_schedules_id_seq'), primary_key=True, nullable=False)

  """Relation to schedules"""
  schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
  schedules = db.relationship('Schedule', backref='weekly_schedules', order_by=id)

  """Relation to days_of_week"""
  day_of_week_id = db.Column(db.Integer, db.ForeignKey('days_of_the_week.id'), nullable=False)
  days_of_week = db.relationship('DayOfTheWeek', backref='weekly_schedules', order_by=id)

  time_of_day = db.Column(db.TIME, nullable=False)
  start_date = db.Column(db.TIMESTAMP(timezone=False), nullable=False)
  end_date = db.Column(db.TIMESTAMP(timezone=False))
  recurrence = db.Column(db.Integer, nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class MonthlySchedule(db.Model):
  __tablename__ = 'monthly_schedules'

  id = db.Column(db.Integer, db.Sequence('monthly_schedules_id_seq'), primary_key=True, nullable=False)

  """Relation to schedules"""
  schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
  schedules = db.relationship('Schedule', backref='monthly_schedules', order_by=id)

  day_of_month = db.Column(db.Integer, nullable=False)
  time_of_day = db.Column(db.TIME, nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class OneTimeSchedule(db.Model):
  __tablename__ = 'one_time_schedules'

  id = db.Column(db.Integer, db.Sequence('one_time_schedules_id_seq'), primary_key=True, nullable=False)

  """Relation to schedules"""
  schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
  schedules = db.relationship('Schedule', backref='one_time_schedules', order_by=id)

  start_date = db.Column(db.TIMESTAMP(timezone=False), nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class Task(db.Model):
  __tablename__ = 'tasks'

  id = db.Column(db.Integer, db.Sequence('tasks_id_seq'), primary_key=True, nullable=False)

  """Relation to schedules"""
  schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
  schedules = db.relationship('Schedule', backref='tasks', order_by=id)

  run_date = db.Column(db.TIMESTAMP(timezone=False), nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class Vulnerability(db.Model):
  __tablename__ = 'vulnerabilities'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.Text, nullable=False)
  cvss_score = db.Column(db.Float, nullable=False)
  bug_id = db.Column(db.Text)
  family = db.Column(db.Text)
  cve_id = db.Column(db.Text)

  """Relation to inventory_hosts"""
  inventory_host_id = db.Column(db.Integer, db.ForeignKey('inventory_hosts.id', ondelete='cascade'))
  inventory_host = db.relationship('InventoryHost', backref='vulnerabilities', order_by=id)

  port = db.Column(db.Text)
  threat_score = db.Column(db.Text)
  severity_score = db.Column(db.Float)
  xrefs = db.Column(db.Text)
  tags = db.Column(db.Text)
  validated = db.Column(db.BOOLEAN),
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)


class ScheduleIndex(db.Model):
  __tablename__ = 'schedules_index'

  id = db.Column(db.Integer, primary_key=True, nullable=False)

  """Relation to schedules"""
  schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
  schedules = db.relationship('Schedule', backref='schedule_index', order_by=id)

  """Relation to targets"""
  target_id = db.Column(db.Integer, db.ForeignKey('targets.id', ondelete='cascade'))
  target = db.relationship('Target', backref='schedule_index', order_by=id)
