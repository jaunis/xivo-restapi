# -*- coding: UTF-8 -*-

# Copyright (C) 2013 Avencall
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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..

import unittest
from flask.testing import FlaskClient

from hamcrest import assert_that, equal_to, has_entries

from xivo_restapi import flask_http_server
from xivo_restapi.helpers import serializer


class TestClient(FlaskClient):

    def open(self, *args, **kwargs):
        kwargs.setdefault('environ_base', {})['REMOTE_ADDR'] = '127.0.0.1'
        return super(FlaskClient, self).open(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        return super(FlaskClient, self).put(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        return super(FlaskClient, self).post(*args, **kwargs)


class TestResources(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        flask_http_server.register_blueprints_v1_1()
        flask_http_server.app.testing = True
        flask_http_server.app.test_client_class = TestClient
        cls.app = flask_http_server.app.test_client()

    def _serialize_encode(self, data):
        return serializer.encode(data).encode('utf8')

    def _serialize_decode(self, data):
        return serializer.decode(data)

    def assert_response(self, response, status_code, expected_response):
        assert_that(status_code, equal_to(response.status_code))
        assert_that(self._serialize_decode(response.data), equal_to(expected_response))

    def assert_response_for_list(self, response, expected_response):
        assert_that(response.status_code, equal_to(200))
        assert_that(self._serialize_decode(response.data), equal_to(expected_response))

    def assert_response_for_get(self, response, expected_response):
        assert_that(response.status_code, equal_to(200))
        assert_that(self._serialize_decode(response.data), has_entries(expected_response))

    def assert_response_for_create(self, response, expected_response):
        assert_that(response.status_code, equal_to(201))
        assert_that(self._serialize_decode(response.data), has_entries(expected_response))

    def assert_response_for_update(self, response):
        assert_that(response.status_code, equal_to(204))
        assert_that(response.data, equal_to(''))

    def assert_response_for_delete(self, response):
        assert_that(response.status_code, equal_to(204))
        assert_that(response.data, equal_to(''))
