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

from flask.globals import request
from flask.helpers import make_response
from xivo_dao.service_data_model.sdm_exception import \
    IncorrectParametersException, MissingParametersException
from xivo_dao.service_data_model.user_sdm import UserSdm
from xivo_restapi.rest import rest_encoder
from xivo_restapi.rest.authentication.xivo_realm_digest import realmDigest
from xivo_restapi.rest.helpers import global_helper
from xivo_restapi.rest.helpers.global_helper import exception_catcher
from xivo_restapi.rest.negotiate.flask_negotiate import produces, consumes
from xivo_restapi.services.user_management import UserManagement
from xivo_restapi.services.utils.exceptions import ProvdError, VoicemailExistsException, SysconfdError
import logging

logger = logging.getLogger(__name__)


class APIUsers(object):

    def __init__(self):
        self._user_management = UserManagement()
        self._user_sdm = UserSdm()

    def _make_response(self, response, code=200):
        encoded = rest_encoder.encode(response)
        return make_response(encoded, code)

    def _decode_request(self):
        decoded = request.data.decode("utf-8")
        return rest_encoder.decode(decoded)

    @exception_catcher
    @produces('application/json')
    @realmDigest.requires_auth
    def list(self):
        logger.info("List of users requested.")
        users = self._user_management.get_all_users()
        response = {"items": users}
        return self._make_response(response)

    @exception_catcher
    @produces('application/json')
    @realmDigest.requires_auth
    def get(self, userid):
        logger.info("User of id %s requested" % userid)
        user = self._user_management.get_user(int(userid))
        return self._make_response(user)

    @exception_catcher
    @consumes('application/json')
    @realmDigest.requires_auth
    def create(self):
        params = self._decode_request()
        logger.info("Request for creating a user with params: %s" % params)
        try:
            self._user_sdm.validate(data)
            user = global_helper.create_class_instance(UserSdm, data)
            self._user_management.create_user(user)
            return self._make_response('', 201)
        except (IncorrectParametersException, MissingParametersException) as e:
            return self._make_response([str(e)], 400)

    @exception_catcher
    @consumes('application/json')
    @realmDigest.requires_auth
    def edit(self, userid):
        params = self._decode_request()
        logger.info("Request for editing the user of id %s with params %s ."
                    % (userid, params))
        try:
            self._user_sdm.validate(data)
            self._user_management.edit_user(int(userid), data)
            return self._make_response('', 200)
        except IncorrectParametersException as e:
            return self._make_response([str(e)], 400)

    @exception_catcher
    @realmDigest.requires_auth
    def delete(self, userid):
        msg = ''
        code = 200

        try:
            delete_voicemail = 'deleteVoicemail' in request.args
            self._user_management.delete_user(int(userid), delete_voicemail)
        except ProvdError as e:
            msg = ["The user was deleted but the device could not be reconfigured (%s)" % str(e)]
            code = 500
        except VoicemailExistsException:
            msg = ["Cannot remove a user with a voicemail. Delete the voicemail or dissociate it from the user."]
            code = 412
        except SysconfdError as e:
            msg = ["The user was deleted but the voicemail content could not be removed  (%s)" % str(e)]
            code = 500

        return self._make_response(msg, code)
