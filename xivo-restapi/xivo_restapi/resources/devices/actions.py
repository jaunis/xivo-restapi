# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging

from . import mapper

from flask import Blueprint, url_for, make_response, request

from xivo_restapi import config
from xivo_restapi.helpers import serializer
from xivo_restapi.helpers.route_generator import RouteGenerator
from xivo_restapi.helpers.formatter import Formatter
from xivo_restapi.helpers.request_bouncer import limit_to_localhost
from xivo_dao.data_handler.device.model import Device
from xivo_dao.data_handler.device import services as device_services
from xivo_dao.data_handler.exception import InvalidParametersError
from xivo_dao.data_handler.line import services as line_services


logger = logging.getLogger(__name__)
blueprint = Blueprint('devices', __name__, url_prefix='/%s/devices' % config.VERSION_1_1)
route = RouteGenerator(blueprint)
formatter = Formatter(mapper, serializer, Device)


@route('/<deviceid>')
def get(deviceid):
    device = device_services.get(deviceid)
    result = formatter.to_api(device)
    return make_response(result, 200)


@route('')
def list():
    find_parameters = _extract_find_parameters()
    search_result = device_services.find_all(**find_parameters)
    result = formatter.list_to_api(search_result.items, search_result.total)
    return make_response(result, 200)


def _extract_find_parameters():
    invalid = []
    parameters = {}

    if 'limit' in request.args:
        limit = request.args['limit']
        if limit.isdigit() and int(limit) > 0:
            parameters['limit'] = int(limit)
        else:
            invalid.append("limit must be a positive number")

    if 'skip' in request.args:
        skip = request.args['skip']
        if skip.isdigit() and int(skip) >= 0:
            parameters['skip'] = int(skip)
        else:
            invalid.append("skip must be a positive number")

    if 'order' in request.args:
        parameters['order'] = request.args['order']

    if 'direction' in request.args:
        parameters['direction'] = request.args['direction']

    if 'search' in request.args:
        parameters['search'] = request.args['search']

    if len(invalid) > 0:
        raise InvalidParametersError(invalid)

    return parameters


@route('', methods=['POST'])
def create():
    data = request.data.decode("utf-8")
    device = formatter.to_model(data)

    created_device = device_services.create(device)

    result = formatter.to_api(created_device)
    location = url_for('.get', deviceid=created_device.id)

    return make_response(result, 201, {'Location': location})


@route('/<deviceid>', methods=['PUT'])
def edit(deviceid):
    data = request.data.decode("utf-8")
    device = device_services.get(deviceid)
    formatter.update_model(data, device)
    device_services.edit(device)
    return make_response('', 204)


@route('/<deviceid>', methods=['DELETE'])
def delete(deviceid):
    device = device_services.get(deviceid)
    device_services.delete(device)
    return make_response('', 204)


@route('/<deviceid>/synchronize')
def synchronize(deviceid):
    device = device_services.get(deviceid)
    device_services.synchronize(device)
    return make_response('', 204)


@route('/<deviceid>/autoprov')
def autoprov(deviceid):
    device = device_services.get(deviceid)
    device_services.reset_to_autoprov(device)
    return make_response('', 204)
