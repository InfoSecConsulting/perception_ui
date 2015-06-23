#!/usr/bin/python
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


class BuildProduct:

    def __init__(self):

        """Build product info from cpe objects"""
        global product_type, product_vendor, product_name, product_version, product_update, product_edition, \
            product_language, product
        try:
            product = self.split(':')
        except AttributeError:
            """Nothing Found"""
        try:
            product_type = product[1]
        except IndexError:
            """Nothing Found"""
        try:
            product_vendor = product[2]
        except IndexError:
            """Nothing Found"""
        try:
            product_name = product[3]
        except IndexError:
            """Nothing Found"""
        try:
            product_version = product[4]
        except IndexError:
            """Nothing Found"""
        try:
            product_update = product[5]
        except IndexError:
            """Nothing Found"""
        try:
            product_edition = product[6]
        except IndexError:
            """Nothing Found"""
        try:
            product_language = product[6]
        except IndexError:
            """Nothing Found"""