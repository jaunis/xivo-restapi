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

from provd.rest.client.client import new_provisioning_client
from urllib2 import URLError
from xivo_dao import user_dao, line_dao, device_dao, voicemail_dao, dialaction_dao
from xivo_dao.mapping_alchemy_sdm.line_mapping import LineMapping
from xivo_dao.mapping_alchemy_sdm.user_mapping import UserMapping
from xivo_restapi.restapi_config import RestAPIConfig
from xivo_restapi.services.utils.exceptions import NoSuchElementException, \
    ProvdError, VoicemailExistsException, SysconfdError
from xivo_restapi.services.utils.sysconfd_connector import SysconfdConnector
from xivo_restapi.services.voicemail_management import VoicemailManagement
import logging

data_access_logger = logging.getLogger(RestAPIConfig.DATA_ACCESS_LOGGERNAME)

logger = logging.getLogger(__name__)


class UserManagement(object):

    def __init__(self):
        self.user_mapping = UserMapping()
        self.line_mapping = LineMapping()
        self.voicemail_manager = VoicemailManagement()
        self.provisioning_client = new_provisioning_client(RestAPIConfig.PROVD_URL)
        self.device_manager = self.provisioning_client.device_manager()
        self.config_manager = self.provisioning_client.config_manager()
        self.sysconfd_connector = SysconfdConnector()

    def get_all_users(self):
        users_lines = user_dao.get_all_join_line()
        return_list = []
        for user, line in users_lines:
            result_user = self.user_mapping.alchemy_to_sdm(user)
            if line is not None:
                result_user.line = self.line_mapping.alchemy_to_sdm(line)
            return_list.append(result_user)
        return return_list

    def get_user(self, userid):
        user = None
        line = None
        result = user_dao.get_user_join_line(userid)
        if result is None:
            raise NoSuchElementException("No such user")
        else:
            user, line = result

        result = self.user_mapping.alchemy_to_sdm(user)
        if line is not None:
            result.line = self.line_mapping.alchemy_to_sdm(line)
        return result

    def create_user(self, user):
        data_access_logger.info("Creating a user with the data %s." % user.todict())
        if not getattr(user, 'description', None):
            user.description = ''
        user_interne = self.user_mapping.sdm_to_alchemy(user)
        self._update_callerid(user_interne)
        user_dao.add_user(user_interne)
        self._add_dialactions(user_interne.id)

    def edit_user(self, userid, data):
        data_access_logger.info("Editing the user of id %s with data %s."
                                % (userid, data))
        alchemy_data = self.user_mapping.sdm_to_alchemy_dict(data)
        updated_rows = user_dao.update(userid, alchemy_data)
        if updated_rows == 0:
            raise NoSuchElementException("No such user")
        if 'lastname' not in data and 'firstname' not in data:
            return
        voicemailid = user_dao.get(userid).voicemailid
        if voicemailid is not None:
            fullname = user_dao.get(userid).fullname
            self.voicemail_manager.edit_voicemail(voicemailid, {'fullname': fullname})

    def delete_user(self, userid, delete_voicemail=False):
        data_access_logger.info("Deleting the user of id %s" % userid)
        try:
            user = user_dao.get(userid)
        except LookupError:
            raise NoSuchElementException("No such user: " + str(userid))
        voicemailid = user.voicemailid
        if voicemailid is not None and not delete_voicemail:
                raise VoicemailExistsException()

        user_dao.delete(userid)
        lines = line_dao.find_line_id_by_user_id(userid)
        if len(lines) > 0:
            self._remove_line(line_dao.get(lines[0]))
        if voicemailid is not None:
            self._delete_voicemail(voicemailid)

    def _provd_remove_line(self, deviceid, linenum):
        config = self.config_manager.get(deviceid)
        del config["raw_config"]["sip_lines"][str(linenum)]
        if len(config["raw_config"]["sip_lines"]) == 0:
            #then we reset to autoprov
            self._reset_config(config)
            self._reset_device_to_autoprov(deviceid)
        self.config_manager.update(config)

    def _reset_config(self, config):
        del config["raw_config"]["sip_lines"]
        if "funckeys" in config["raw_config"]:
            del config["raw_config"]["funckeys"]

    def _reset_device_to_autoprov(self, deviceid):
        device = self.device_manager.get(deviceid)
        new_configid = self.config_manager.autocreate()
        device["config"] = new_configid
        self.device_manager.update(device)

    def _remove_line(self, line):
        device = line.device
        line_dao.delete(line.id)
        deviceid = device_dao.get_deviceid(device)
        if deviceid is not None:
            try:
                self._provd_remove_line(deviceid, line.num)
            except URLError as e:
                raise ProvdError(str(e))

    def _delete_voicemail(self, voicemailid):
        voicemail = voicemail_dao.get(voicemailid)
        context, mailbox = voicemail.context, voicemail.mailbox
        voicemail_dao.delete(voicemailid)
        try:
            self.sysconfd_connector.delete_voicemail_storage(context, mailbox)
        except Exception as e:
            raise SysconfdError(str(e))

    def _update_callerid(self, user):
        fullname = user.firstname
        if user.lastname:
            fullname += " %s" % user.lastname

        user.callerid = '"%s"' % fullname

    def _add_dialactions(self, user_id):
        for event in ['noanswer', 'busy', 'congestion', 'chanunavail']:
            dialaction_dao.add_dialaction_for_user(user_id, event)
