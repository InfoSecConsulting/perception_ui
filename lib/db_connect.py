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

from os import system
import sys
import lib.yml_parser as parse_yml


try:
    import sqlalchemy
    from sqlalchemy import Column, String, Text, Integer, ForeignKey, Sequence, create_engine, MetaData
    from sqlalchemy.orm import relationship, sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.engine.url import URL
except ImportError:
    print('Installing SQLAlchemy, psycopg2, and alembic with PIP3')
    system('pip3 install SQLAlchemy')
    system('pip3 install psycopg2')
    system('pip3 install alembic')
    import sqlalchemy
    from sqlalchemy import Column, String, Text, Integer, ForeignKey, Sequence, create_engine, MetaData
    from sqlalchemy.orm import relationship, sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.engine.url import URL

Session = sessionmaker()


def connect():
  db_yml = 'config/database.yml'
  db_info = parse_yml.db_info(db_yml)
  cursor = None

  try:
    Session = sessionmaker()
    engine = create_engine(URL(**db_info), pool_size=20)
    Session.configure(bind=engine)
    return Session
  except sqlalchemy.exc.OperationalError as e:
    print(e)
    sys.exit(1)
  finally:
    if cursor:
      cursor.close()
