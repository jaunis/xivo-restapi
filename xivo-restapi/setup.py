#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (C) 2012  Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


from distutils.core import setup

setup(
    name='xivo-restapid',
    version='0.1',
    description='XIVO REST API daemon',
    author='Avencall',
    author_email='xivo-dev@lists.proformatique.com',
    url='http://git.xivo.fr/',
    license='GPLv3',
    packages=[
        'xivo_restapi',
        'xivo_restapi.authentication',
        'xivo_restapi.authentication.werkzeug',
        'xivo_restapi.helpers',
        'xivo_restapi.negotiate',
        'xivo_restapi.resources',
        'xivo_restapi.resources.call_logs',
        'xivo_restapi.resources.devices',
        'xivo_restapi.resources.extensions',
        'xivo_restapi.resources.lines',
        'xivo_restapi.resources.user_links',
        'xivo_restapi.resources.users',
        'xivo_restapi.resources.voicemails',
        'xivo_restapi.v1_0',
        'xivo_restapi.v1_0.mapping_alchemy_sdm',
        'xivo_restapi.v1_0.rest',
        'xivo_restapi.v1_0.rest.helpers',
        'xivo_restapi.v1_0.service_data_model',
        'xivo_restapi.v1_0.services',
        'xivo_restapi.v1_0.services.utils',
    ],
    scripts=[
        'bin/xivo-restapid'
    ],
)
