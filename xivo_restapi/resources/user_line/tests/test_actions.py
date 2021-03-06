# -*- coding: utf-8 -*-
#
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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from hamcrest import assert_that, equal_to

from mock import patch
from xivo_dao.data_handler.user_line.model import UserLine
from xivo_dao.data_handler.user_line.exception import UserLineNotExistsError
from xivo_dao.data_handler.user.model import User
from xivo_dao.data_handler.exception import ElementNotExistsError
from xivo_restapi.helpers.tests.test_resources import TestResources


BASE_URL = '/1.1/users/%s/lines'
DISSOCIATE_URL = BASE_URL + '/%s'


class TestUserLineActions(TestResources):

    def setUp(self):
        super(TestUserLineActions, self).setUp()
        self.user_line = UserLine(user_id=1, line_id=2)

    def build_item(self, user_line):
        item = {
            u'user_id': user_line.user_id,
            u'line_id': user_line.line_id,
            u'main_user': user_line.main_user,
            u'main_line': user_line.main_line,
            'links': [
                {
                    'rel': 'lines',
                    'href': 'http://localhost/1.1/lines/%s' % user_line.line_id
                },
                {
                    u'href': u'http://localhost/1.1/users/%d' % user_line.user_id,
                    u'rel': u'users'
                }
            ]
        }

        return item

    @patch('xivo_dao.data_handler.user_line.services.associate')
    def test_associate_line(self, user_line_associate):
        user_line_associate.return_value = self.user_line

        expected_result = self.build_item(self.user_line)

        data = {'line_id': self.user_line.line_id}
        data_serialized = self._serialize_encode(data)

        result = self.app.post(BASE_URL % self.user_line.user_id, data=data_serialized)

        self.assert_response_for_create(result, expected_result)
        user_line_associate.assert_called_once_with(self.user_line)

    @patch('xivo_dao.data_handler.user_line.services.get_by_user_id_and_line_id')
    @patch('xivo_dao.data_handler.user_line.services.dissociate')
    def test_dissociate_line(self, user_line_dissociate, get_by_user_id_and_line_id):
        get_by_user_id_and_line_id.return_value = self.user_line

        result = self.app.delete(DISSOCIATE_URL % (self.user_line.user_id,
                                                   self.user_line.line_id))

        self.assert_response_for_delete(result)
        get_by_user_id_and_line_id.assert_called_once_with(self.user_line.user_id, self.user_line.line_id)
        user_line_dissociate.assert_called_once_with(self.user_line)

    @patch('xivo_dao.data_handler.user_line.services.get_by_user_id_and_line_id')
    def test_dissociate_line_when_user_line_does_not_exist(self, get_by_user_id_and_line_id):
        expected_status_code = 404
        expected_response = ['User with id=%s is not associated with line id=%s' % (self.user_line.user_id, self.user_line.line_id)]

        get_by_user_id_and_line_id.side_effect = UserLineNotExistsError.from_user_id(self.user_line.user_id)

        result = self.app.delete(DISSOCIATE_URL % (self.user_line.user_id, self.user_line.line_id))

        get_by_user_id_and_line_id.assert_called_once_with(self.user_line.user_id, self.user_line.line_id)

        assert_that(result.status_code, equal_to(expected_status_code))
        assert_that(self._serialize_decode(result.data), equal_to(expected_response))

    @patch('xivo_dao.data_handler.user.services.get')
    def test_get_line_associated_to_a_user_when_user_does_not_exist(self, user_services_get):
        expected_status_code = 404
        expected_result = ["User with id=1 does not exist"]

        user_services_get.side_effect = ElementNotExistsError('User', id=self.user_line.user_id)

        result = self.app.get(BASE_URL % self.user_line.user_id)

        assert_that(result.status_code, equal_to(expected_status_code))
        assert_that(self._serialize_decode(result.data), equal_to(expected_result))

    @patch('xivo_dao.data_handler.user.services.get')
    @patch('xivo_dao.data_handler.user_line.services.find_all_by_user_id')
    def test_get_lines_associated_to_a_user_with_no_line(self, user_line_find_all_by_user_id, user_services_get):
        user_services_get.return_value = User(id=self.user_line.user_id)
        user_line_find_all_by_user_id.return_value = []

        expected_result = {u'items': [], u'total': 0}

        result = self.app.get(BASE_URL % self.user_line.user_id)

        self.assert_response_for_list(result, expected_result)

    @patch('xivo_dao.data_handler.user.services.get')
    @patch('xivo_dao.data_handler.user_line.services.find_all_by_user_id')
    def test_get_lines_associated_to_a_user(self, user_line_find_all_by_user_id, user_services_get):
        user_services_get.return_value = User(id=self.user_line.user_id)
        user_line_find_all_by_user_id.return_value = [self.user_line]

        expected_result = {
            u'total': 1,
            u'items': [self.build_item(self.user_line)]
        }

        result = self.app.get(BASE_URL % self.user_line.user_id)

        self.assert_response_for_list(result, expected_result)
