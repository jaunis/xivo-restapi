# -*- coding: UTF-8 -*-
#
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

from flask import Blueprint
from xivo_restapi.rest.API_agents import APIAgents
from xivo_restapi.rest.API_campaigns import APICampaigns
from xivo_restapi.rest.API_queues import APIQueues
from xivo_restapi.rest.API_recordings import APIRecordings
from xivo_restapi.rest.API_users import APIUsers
from xivo_restapi.rest.API_voicemails import APIVoicemails
from xivo_restapi.restapi_config import RestAPIConfig
import logging

logger = logging.getLogger(__name__)

root = Blueprint("root",
                 __name__,
                 url_prefix=RestAPIConfig.XIVO_REST_SERVICE_ROOT_PATH +
                            RestAPIConfig.XIVO_RECORDING_SERVICE_PATH)

# ****************** #
#   API campaigns    #
# ****************** #

root.add_url_rule("/",
                  "get",
                  getattr(APICampaigns(), "get"),
                  methods=["GET"])

root.add_url_rule("/<campaign_id>",
                  "get",
                  getattr(APICampaigns(), "get"),
                  methods=["GET"])

root.add_url_rule('/',
                  "add_campaign",
                  getattr(APICampaigns(), "add_campaign"),
                  methods=['POST'])

root.add_url_rule('/<campaign_id>',
                  "update",
                  getattr(APICampaigns(), "update"),
                  methods=['PUT'])

root.add_url_rule("/<campaign_id>",
                  "delete_campaign",
                  getattr(APICampaigns(), "delete"),
                  methods=['DELETE'])


# ****************** #
#   API recordings   #
# ****************** #
root.add_url_rule("/<campaign_id>/search",
                  "search_recording",
                  getattr(APIRecordings(), "search"),
                  methods=["GET"])

root.add_url_rule("/<campaign_id>/",
                  "list_recordings",
                  getattr(APIRecordings(), "list_recordings"),
                  methods=["GET"])

root.add_url_rule("/<campaign_id>/",
                  "add_recording",
                  getattr(APIRecordings(), "add_recording"),
                  methods=["POST"])

root.add_url_rule("/<campaign_id>/<recording_id>",
                  "delete",
                  getattr(APIRecordings(), "delete"),
                  methods=["DELETE"])


# ****************** #
#   Queues server    #
# ****************** #
queues_service = Blueprint("queues_service",
                         __name__,
                         url_prefix=RestAPIConfig.XIVO_REST_SERVICE_ROOT_PATH +
                                    RestAPIConfig.XIVO_QUEUES_SERVICE_PATH)

# ****************** #
#   API queues       #
# ****************** #

queues_service.add_url_rule("/",
                  "list_queues",
                  getattr(APIQueues(), "list_queues"),
                  methods=["GET"])


# ****************** #
#   Agents server    #
# ****************** #
agents_service = Blueprint("agents_service",
                         __name__,
                         url_prefix=RestAPIConfig.XIVO_REST_SERVICE_ROOT_PATH +
                                    RestAPIConfig.XIVO_AGENTS_SERVICE_PATH)

# ****************** #
#   API agents       #
# ****************** #

agents_service.add_url_rule("/",
                  "list_agents",
                  getattr(APIAgents(), "list_agents"),
                  methods=["GET"])

# ****************** #
#   Users server     #
# ****************** #
users_service = Blueprint("users_service",
                         __name__,
                         url_prefix=RestAPIConfig.XIVO_REST_SERVICE_ROOT_PATH +
                                    RestAPIConfig.XIVO_USERS_SERVICE_PATH)
# *************** #
#   API users     #
# *************** #

users_service.add_url_rule("/",
                           "list",
                           getattr(APIUsers(), "list"),
                           methods=["GET"])

users_service.add_url_rule("/<userid>",
                  "get",
                  getattr(APIUsers(), "get"),
                  methods=["GET"])

users_service.add_url_rule("/",
                  "create",
                  getattr(APIUsers(), "create"),
                  methods=["POST"])

users_service.add_url_rule("/<userid>",
                  "edit",
                  getattr(APIUsers(), "edit"),
                  methods=["PUT"])

users_service.add_url_rule("/<userid>/enablednd",
                  "enablednd",
                  getattr(APIUsers(), "enablednd"),
                  methods=["POST"])

users_service.add_url_rule("/<userid>/disablednd",
                  "disablednd",
                  getattr(APIUsers(), "disablednd"),
                  methods=["POST"])

# ********************* #
#   Voicemails server   #
# ********************* #
voicemails_service = Blueprint("voicemails_service",
                         __name__,
                         url_prefix=RestAPIConfig.XIVO_REST_SERVICE_ROOT_PATH +
                                    RestAPIConfig.XIVO_VOICEMAIL_SERVICE_PATH)

# ******************** #
#   API voicemails     #
# ******************** #

voicemails_service.add_url_rule("/",
                  "list",
                  getattr(APIVoicemails(), "list"),
                  methods=["GET"])

voicemails_service.add_url_rule("/<voicemailid>",
                  "edit",
                  getattr(APIVoicemails(), "edit"),
                  methods=["PUT"])
