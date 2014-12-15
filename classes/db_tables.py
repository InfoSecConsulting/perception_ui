#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
(C) Copyright [2014] Avery Rozar

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
__author__ = 'Avery Rozar'

from sqlalchemy import Column, Integer, Text, ForeignKey, Sequence, TIMESTAMP, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from base.Base import Base
import datetime


def _get_date():
    return datetime.datetime.now()


class NvdVuln(Base):
    __tablename__ = 'nvd_vulns'

    id = Column(Integer, Sequence('nvd_vulns_id_seq'), primary_key=True, nullable=False)
    name = Column(Text, unique=True, nullable=False)

    """Relation to tie products to vulnerabilities from the NVD"""
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', backref='nvd_vulns', order_by=id)

    cveid = Column(Text, nullable=False)
    vuln_published = Column(Text)
    vuln_updated = Column(Text)
    cvss = Column(Text)
    cweid = Column(Text)

    """Relation to tie references to vulnerabilities from the NVD"""
    nvd_vuln_reference_id = Column(Integer, ForeignKey('nvd_vuln_references.id'))
    nvd_vuln_reference = relationship('NvdVulnReference', backref='nvd_vulns', order_by=id)

    summary = Column(Text)
    created_at = Column(TIMESTAMP(timezone=False))
    updated_at = Column(TIMESTAMP(timezone=False))


class HostNseScript(Base):
    __tablename__ = 'host_nse_scripts'

    id = Column(Integer, Sequence('host_nse_scripts_id_seq'), primary_key=True, nullable=False)

    """Relation to host"""
    host_id = Column(Integer, ForeignKey('inventory_hosts.id'))
    host = relationship('InventoryHost', backref='host_nse_scripts', order_by=id)

    name = Column(Text, nullable=False)
    output = Column(Text, nullable=False)


class SvcNseScript(Base):
    __tablename__ = 'svc_nse_scripts'

    id = Column(Integer, Sequence('svc_nse_scripts_id_seq'), primary_key=True, nullable=False)

    """Relation to host"""
    svc_id = Column(Integer, ForeignKey('inventory_svcs.id', ondelete='cascade'))
    svc = relationship('InventorySvc', backref='svc_nse_scripts', order_by=id)

    name = Column(Text, nullable=False)
    output = Column(Text, nullable=False)


class Vendor(Base):
    __tablename__ = 'vendors'

    id = Column(Integer, Sequence('vendors_id_seq'), primary_key=True, nullable=False)
    name = Column(Text, unique=True, nullable=False)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('products_id_seq'), primary_key=True, nullable=False)

    product_type = Column(Text, nullable=False)

    """Relation to tie vendors to products"""
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    vendor = relationship('Vendor', backref='products', order_by=id)

    name = Column(Text, nullable=False)
    version = Column(Text)
    product_update = Column(Text)
    edition = Column(Text)
    language = Column(Text)


class NvdVulnReference(Base):
    __tablename__ = 'nvd_vuln_references'

    id = Column(Integer, Sequence('nvd_vuln_references_id_seq'), primary_key=True, nullable=False)

    """Relation to tie vulnerability source disclosure to NVD vulnerabilities"""
    nvd_vuln_source_id = Column(Integer, ForeignKey('nvd_vuln_sources.id'), nullable=False)
    nvd_vuln_source = relationship('NvdVulnSource', backref='nvd_vuln_references', order_by=id)

    type = Column(Text)
    href = Column(Text)


class NvdVulnSource(Base):
    __tablename__ = 'nvd_vuln_sources'

    id = Column(Integer, Sequence('nvd_vuln_sources_id_seq'), primary_key=True, nullable=False)
    name = Column(Text)


class InventoryHost(Base):
    __tablename__ = 'inventory_hosts'

    id = Column(Integer, Sequence('inventory_hosts_id_seq'), primary_key=True, nullable=False)
    ipv4_addr = Column(postgresql.INET, unique=True)
    ipv6_addr = Column(postgresql.INET)
    macaddr = Column(postgresql.MACADDR)

    """Relation to tie mac address vendors to inventory hosts"""
    mac_vendor_id = Column(Integer, ForeignKey('mac_vendors.id'))
    mac_vendor = relationship('MACVendor', backref='inventory_hosts', order_by=id)

    state = Column(Text)
    host_name = Column(Text)

    """Relation to tie an OS inventory hosts"""
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product', backref='inventory_hosts', order_by=id)

    arch = Column(Text)

    """Relation to tie users to inventory hosts"""
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='inventory_hosts', order_by=id)

    info = Column(Text)
    comments = Column(Text)

    """Relation to tie NVD vulnerabilities to inventory hosts"""
    nvd_vuln_id = Column(Integer, ForeignKey('nvd_vulns.id'))
    nvd_vuln = relationship('NvdVuln', backref='inventory_hosts', order_by=id)

    created_at = Column(TIMESTAMP(timezone=False), default=_get_date)
    updated_at = Column(TIMESTAMP(timezone=False), onupdate=_get_date)


class InventorySvc(Base):
    __tablename__ = 'inventory_svcs'

    id = Column(Integer, Sequence('inventory_svcs_id_seq'), primary_key=True, nullable=False)

    """Relation to inventory hosts"""
    host_id = Column(Integer, ForeignKey('inventory_hosts.id'))
    host = relationship('InventoryHost', backref='inventory_svcs', order_by=id)

    protocol = Column(Text)
    portid = Column(Integer)
    name = Column(Text)
    svc_product = Column(Text)
    extra_info = Column(Text)

    """Relation to tie products to inventory services"""
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product', backref='inventory_svcs', order_by=id)

    created_at = Column(TIMESTAMP(timezone=False), default=_get_date)


class MACVendor(Base):
    __tablename__ = 'mac_vendors'

    id = Column(Integer, Sequence('mac_vendors_id_seq'), primary_key=True, nullable=False)
    name = Column(Text, unique=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String)
    encrypted_password = Column(String)
    encrypted_enable_password = Column(String)

    created_at = Column(TIMESTAMP(timezone=False), default=_get_date)
    updated_at = Column(TIMESTAMP(timezone=False), onupdate=_get_date)