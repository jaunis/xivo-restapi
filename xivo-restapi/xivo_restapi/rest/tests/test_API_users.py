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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..

import unittest

from mock import Mock, patch
from xivo_dao.alchemy.userfeatures import UserFeatures
from xivo_dao.service_data_model.sdm_exception import \
    IncorrectParametersException, MissingParametersException
from xivo_dao.service_data_model.user_sdm import UserSdm
from xivo_restapi.rest import rest_encoder
from xivo_restapi.rest.helpers import global_helper
from xivo_restapi.restapi_config import RestAPIConfig
from xivo_restapi.services.user_management import UserManagement
from xivo_restapi.services.utils.exceptions import NoSuchElementException, \
    ProvdError, VoicemailExistsException, SysconfdError
from xivo_restapi.rest import flask_http_server

BASE_URL = "%s%s" % (RestAPIConfig.XIVO_REST_SERVICE_ROOT_PATH, RestAPIConfig.XIVO_USERS_SERVICE_PATH)


class TestAPIUsers(unittest.TestCase):

    def setUp(self):
        self.patcher_users = patch("xivo_restapi.rest.API_users.UserManagement")
        mock_user = self.patcher_users.start()
        self.instance_user_management = Mock(UserManagement)
        mock_user.return_value = self.instance_user_management

        self.patcher_user_sdm = patch("xivo_restapi.rest.API_users.UserSdm")
        self.mock_user_sdm = self.patcher_user_sdm.start()
        self.user_sdm = Mock(UserSdm)
        self.mock_user_sdm.return_value = self.user_sdm
        flask_http_server.register_blueprints()
        flask_http_server.app.testing = True
        self.app = flask_http_server.app.test_client()

    def tearDown(self):
        self.patcher_user_sdm.stop()
        self.patcher_users.stop()

    def test_list_users(self):
        status = "200 OK"
        user1 = UserFeatures()
        user1.firstname = 'test1'
        user2 = UserFeatures()
        user2.firstname = 'test2'
        expected_list = [user1, user2]
        expected_result = {"items": expected_list}
        self.instance_user_management.get_all_users.return_value = expected_list

        result = self.app.get("%s/" % BASE_URL, '')

        self.instance_user_management.get_all_users.assert_any_call()
        self.assertEquals(result.status, status)
        self.assertEquals(rest_encoder.encode(expected_result), result.data)

    def test_list_users_error(self):
        status = "500 INTERNAL SERVER ERROR"
        self.instance_user_management.get_all_users.side_effect = Exception

        result = self.app.get("%s/" % BASE_URL)

        self.instance_user_management.get_all_users.assert_any_call()
        self.assertEqual(result.status, status)
        self.instance_user_management.get_all_users.side_effect = None

    def test_get(self):
        status = "200 OK"
        user1 = UserFeatures()
        user1.firstname = 'test1'
        self.instance_user_management.get_user.return_value = user1

        result = self.app.get("%s/1" % BASE_URL, '')

        self.instance_user_management.get_user.assert_called_with(1)
        self.assertEquals(result.status, status)
        self.assertEquals(rest_encoder.encode(user1), result.data)

    def test_get_error(self):
        status = "500 INTERNAL SERVER ERROR"
        self.instance_user_management.get_user.side_effect = Exception

        result = self.app.get("%s/1" % BASE_URL)

        self.instance_user_management.get_user.assert_called_with(1)
        self.assertEqual(result.status, status)
        self.instance_user_management.get_user.side_effect = None

    def test_get_not_found(self):
        status = "404 NOT FOUND"

        self.instance_user_management.get_user.side_effect = NoSuchElementException("No such user")

        result = self.app.get("%s/1" % BASE_URL)

        self.instance_user_management.get_user.assert_called_with(1)
        self.assertEqual(result.status, status)
        self.instance_user_management.get_user.side_effect = None

    def test_create(self):
        status = "201 CREATED"
        data = {u'firstname': u'André',
                u'lastname': u'Dupond',
                u'description': u'éà":;'}
        self.instance_user_management.create_user.return_value = True
        global_helper.create_class_instance = Mock()
        global_helper.create_class_instance.return_value = self.user_sdm

        result = self.app.post("%s/" % BASE_URL, data=rest_encoder.encode(data))

        self.assertEqual(result.status, status)
        global_helper.create_class_instance.assert_called_with(self.mock_user_sdm, data)
        self.instance_user_management.create_user.assert_called_with(self.user_sdm)

    def test_create_no_parameters(self):
        status = "400 BAD REQUEST"
        expected_data = "Missing parameters sent: firstname"
        data = {}
        self.user_sdm.validate.side_effect = MissingParametersException("firstname")

        result = self.app.post("%s/" % BASE_URL, data=rest_encoder.encode(data))

        self.assertEqual(status, result.status)
        received_data = rest_encoder.decode(result.data)
        self.assertEquals(expected_data, received_data[0])
        self.user_sdm.validate.side_effect = None

    def test_create_empty_firstname(self):
        status = "400 BAD REQUEST"
        expected_data = "Missing parameters sent: firstname"
        data = {'firstname': ''}
        self.user_sdm.validate.side_effect = MissingParametersException("firstname")

        result = self.app.post("%s/" % BASE_URL, data=rest_encoder.encode(data))

        self.assertEqual(status, result.status)
        received_data = rest_encoder.decode(result.data)
        self.assertEquals(expected_data, received_data[0])
        self.user_sdm.validate.side_effect = None

    def test_create_error(self):
        status = "500 INTERNAL SERVER ERROR"
        data = {'firstname': 'André',
                'lastname': 'Dupond',
                'description': 'éà":;'}

        self.instance_user_management.create_user.side_effect = Exception

        result = self.app.post("%s/" % BASE_URL, data=rest_encoder.encode(data))

        self.assertEqual(status, result.status)
        self.instance_user_management.create_user.side_effect = None

    def test_create_request_error(self):
        status = "400 BAD REQUEST"
        expected_data = "Incorrect parameters sent: unexisting_field"
        data = {'firstname': 'André',
                'lastname': 'Dupond',
                'unexisting_field': 'value'}
        self.user_sdm.validate.side_effect = IncorrectParametersException("unexisting_field")

        result = self.app.post("%s/" % BASE_URL, data=rest_encoder.encode(data))

        self.assertEqual(status, result.status)
        received_data = rest_encoder.decode(result.data)
        self.assertEquals(expected_data, received_data[0])
        self.user_sdm.validate.side_effect = None

    def test_edit(self):
        status = "200 OK"
        data = {u'id': 2,
                u'firstname': u'André',
                u'lastname': u'Dupond',
                u'description': u'éà":;'}
        self.instance_user_management.edit_user.return_value = True
        self.user_sdm.validate.return_value = True

        result = self.app.put("%s/1" % BASE_URL, data=rest_encoder.encode(data))

        self.assertEqual(result.status, status)
        self.user_sdm.validate.assert_called_with(data)
        self.instance_user_management.edit_user.assert_called_with(1, data)

    def test_edit_error(self):
        status = "500 INTERNAL SERVER ERROR"
        data = {u'firstname': u'André',
                u'lastname': u'Dupond',
                u'description': u'éà":;'}
        self.instance_user_management.edit_user.side_effect = Exception

        result = self.app.put("%s/1" % BASE_URL, data=rest_encoder.encode(data))

        self.user_sdm.validate.assert_called_with(data)
        self.assertEqual(status, result.status)
        self.instance_user_management.edit_user.side_effect = None

    def test_edit_request_error(self):
        status = "400 BAD REQUEST"
        expected_data = "Incorrect parameters sent: unexisting_field"
        data = {u'firstname': u'André',
                u'lastname': u'Dupond',
                u'unexisting_field': u'value'}
        self.user_sdm.validate.side_effect = IncorrectParametersException("unexisting_field")

        result = self.app.put("%s/1" % BASE_URL, data=rest_encoder.encode(data))

        self.assertEquals(result.status, status)
        received_data = rest_encoder.decode(result.data)
        self.assertEquals(received_data[0], expected_data)
        self.user_sdm.validate.assert_called_with(data)
        self.instance_user_management.edit_user.side_effect = None

    def test_edit_not_found(self):
        status = "404 NOT FOUND"
        data = {'firstname': 'André',
                'lastname': 'Dupond',
                'description': 'éà":;'}

        self.instance_user_management.edit_user.side_effect = NoSuchElementException('')

        result = self.app.put("%s/1" % BASE_URL, data=rest_encoder.encode(data))

        self.assertEqual(status, result.status)
        self.instance_user_management.edit_user.side_effect = None

    def test_delete_success(self):
        status = "200 OK"
        self.instance_user_management.delete_user.return_value = True

        result = self.app.delete("%s/1" % BASE_URL)

        self.assertEqual(result.status, status)
        self.instance_user_management.delete_user.assert_called_with(1, False)

    def test_delete_not_found(self):
        status = "404 NOT FOUND"

        self.instance_user_management.delete_user.side_effect = NoSuchElementException("")

        result = self.app.delete("%s/1" % BASE_URL)

        self.assertEqual(result.status, status)
        self.instance_user_management.delete_user.assert_called_with(1, False)

        self.instance_user_management.delete_user.side_effect = None

    def test_delete_provd_error(self):
        status = "500 INTERNAL SERVER ERROR"

        self.instance_user_management.delete_user.side_effect = ProvdError("sample error")

        result = self.app.delete("%s/1" % BASE_URL)

        self.instance_user_management.delete_user.side_effect = None
        self.assertEqual(result.status, status)
        data = rest_encoder.decode(result.data)

        expected_msg = "The user was deleted but the device could not be reconfigured (provd error: sample error)"
        self.assertEquals(expected_msg, data[0])

        self.instance_user_management.delete_user.assert_called_with(1, False)

    def test_delete_voicemail_exists(self):
        status = "412 PRECONDITION FAILED"

        self.instance_user_management.delete_user.side_effect = VoicemailExistsException

        result = self.app.delete("%s/1" % BASE_URL)

        self.instance_user_management.delete_user.side_effect = None
        self.assertEqual(result.status, status)
        data = rest_encoder.decode(result.data)

        expected_msg = "Cannot remove a user with a voicemail. Delete the voicemail or dissociate it from the user."
        self.assertEquals(expected_msg, data[0])
        self.instance_user_management.delete_user.assert_called_with(1, False)

    def test_delete_force_voicemail_deletion(self):
        status = "200 OK"

        result = self.app.delete("%s/1?deleteVoicemail" % BASE_URL)

        self.assertEqual(result.status, status)
        self.instance_user_management.delete_user.assert_called_with(1, True)

    def test_delete_sysconfd_error(self):
        status = "500 INTERNAL SERVER ERROR"

        self.instance_user_management.delete_user.side_effect = SysconfdError("sample error")

        result = self.app.delete("%s/1" % BASE_URL)

        self.instance_user_management.delete_user.side_effect = None
        self.assertEqual(result.status, status)
        data = rest_encoder.decode(result.data)

        expected_msg = "The user was deleted but the voicemail content could not be removed  (sysconfd error: sample error)"
        self.assertEquals(expected_msg, data[0])
        self.instance_user_management.delete_user.assert_called_with(1, False)
