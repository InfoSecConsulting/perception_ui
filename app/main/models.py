from app import db
from sqlalchemy.dialects import postgresql
import datetime


def _get_date():
    return datetime.datetime.now()


class Vendor(db.Model):
  __tablename__ = 'vendors'

  id = db.Column(db.Integer, db.Sequence('vendors_id_seq'), primary_key=True, nullable=False)
  name = db.Column(db.Text, unique=True, nullable=False)


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


class NvdVulnSource(db.Model):
  __tablename__ = 'nvd_vuln_sources'

  id = db.Column(db.Integer, db.Sequence('nvd_vuln_sources_id_seq'), primary_key=True, nullable=False)
  name = db.Column(db.Text)


class NvdVulnReference(db.Model):
  __tablename__ = 'nvd_vuln_references'

  id = db.Column(db.Integer, db.Sequence('nvd_vuln_references_id_seq'), primary_key=True, nullable=False)

  """Relation to tie vulnerability source disclosure to NVD vulnerabilities"""
  nvd_vuln_source_id = db.Column(db.Integer, db.ForeignKey('nvd_vuln_sources.id'), nullable=False)
  nvd_vuln_source = db.relationship('NvdVulnSource', backref='nvd_vuln_references', order_by=id)

  nvd_ref_type = db.Column(db.Text)
  href = db.Column(db.Text)


class NvdVuln(db.Model):
  __tablename__ = 'nvd_vulns'

  id = db.Column(db.Integer, db.Sequence('nvd_vulns_id_seq'), primary_key=True, nullable=False)
  name = db.Column(db.Text, unique=True, nullable=False)

  """Relation to tie products to vulnerabilities from the NVD"""
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
  product = db.relationship('Product', backref='nvd_vulns', order_by=id)

  cveid = db.Column(db.Text, nullable=False)
  vuln_published = db.Column(db.Text)
  vuln_updated = db.Column(db.Text)
  cvss = db.Column(db.Text)
  cweid = db.Column(db.Text)

  """Relation to tie references to vulnerabilities from the NVD"""
  nvd_vuln_reference_id = db.Column(db.Integer, db.ForeignKey('nvd_vuln_references.id'))
  nvd_vuln_reference = db.relationship('NvdVulnReference', backref='nvd_vulns', order_by=id)

  summary = db.Column(db.Text)
  created_at = db.Column(db.TIMESTAMP(timezone=False))
  updated_at = db.Column(db.TIMESTAMP(timezone=False))


class MACVendor(db.Model):
  __tablename__ = 'mac_vendors'

  id = db.Column(db.Integer, db.Sequence('mac_vendors_id_seq'), primary_key=True, nullable=False)
  name = db.Column(db.Text, unique=True)


class SmbUser(db.Model):
  __tablename__ = 'smb_users'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  username = db.Column(db.String)
  encrypted_password = db.Column(db.String)

  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


class LinuxUser(db.Model):
  __tablename__ = 'linux_users'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  username = db.Column(db.String)
  encrypted_password = db.Column(db.String)
  encrypted_enable_password = db.Column(db.String)

  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
  updated_at = db.Column(db.TIMESTAMP(timezone=False), onupdate=_get_date)


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

  """Relation to tie NVD vulnerabilities to inventory hosts"""
  nvd_vuln_id = db.Column(db.Integer, db.ForeignKey('nvd_vulns.id'))
  nvd_vuln = db.relationship('NvdVuln', backref='inventory_hosts', order_by=id)

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


class SvcNseScript(db.Model):
  __tablename__ = 'svc_nse_scripts'

  id = db.Column(db.Integer, db.Sequence('svc_nse_scripts_id_seq'), primary_key=True, nullable=False)

  """Relation to inventory_svc"""
  inventory_svc_id = db.Column(db.Integer, db.ForeignKey('inventory_svcs.id', ondelete='cascade'))
  inventory_svc = db.relationship('InventorySvc', backref='svc_nse_scripts', order_by=id)

  name = db.Column(db.Text, nullable=False)
  output = db.Column(db.Text, nullable=False)


class LocalNet(db.Model):
  __tablename__ = 'local_nets'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  subnet = db.Column(postgresql.CIDR, unique=True)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)


class DiscoveryProtocolFindings(db.Model):
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


class LocalHosts(db.Model):
  __tablename__ = 'local_hosts'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  ip_addr = db.Column(postgresql.INET, unique=True, nullable=False)
  mac_addr = db.Column(postgresql.MACADDR, unique=True, nullable=False)
  created_at = db.Column(db.TIMESTAMP(timezone=False), default=_get_date)
