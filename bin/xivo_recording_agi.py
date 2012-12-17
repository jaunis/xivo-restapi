#!/usr/bin/python
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

from gevent import httplib
from xivo.agi import AGI
from xivo_recording.recording_config import RecordingConfig
from xivo_recording.rest import rest_encoder
import logging
import sys
from time import localtime, strftime

DEBUG_MODE = False
LOGFILE = '/var/log/xivo_recording_agi'

REST_ERROR = 1

agi = None
logger = None


class RestAPIError(Exception):
    pass

class AGIError(Exception):
    pass

def get_variables():

    QUEUE_NAME = agi.get_variable('XIVO_QUEUENAME')

    return QUEUE_NAME


def add_recording_detail(campaign_details):
    connection = httplib.HTTPConnection(
                            RecordingConfig.XIVO_RECORD_SERVICE_ADDRESS +
                            ":" +
                            str(RecordingConfig.XIVO_RECORD_SERVICE_PORT)
                        )

    requestURI = RecordingConfig.XIVO_REST_SERVICE_ROOT_PATH + \
                    RecordingConfig.XIVO_RECORDING_SERVICE_PATH + "/" + \
                    str(campaign_details['campaign_name']) + '/'

    global agi
    if agi == None:
        raise AGIError()

    body = {}
    body['cid'] = agi.get_variable('UNIQUEID')
    body['caller'] = agi.get_variable('XIVO_SRCNUM')
    body['callee'] = agi.get_variable('XIVO_DSTNUM')
    body['start_time'] = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    body['agent'] = agi.get_variable('6004')
    body_json = rest_encoder.encode(body)
    headers = RecordingConfig.CTI_REST_DEFAULT_CONTENT_TYPE

    connection.request("POST", requestURI, body_json, headers)

    reply = connection.getresponse()

    if (reply.status != "201"):
        raise RestAPIError()

    return reply.read()


def get_campaigns(queue_name):
    connection = httplib.HTTPConnection(
                            RecordingConfig.XIVO_RECORD_SERVICE_ADDRESS +
                            ":" +
                            str(RecordingConfig.XIVO_RECORD_SERVICE_PORT)
                        )

    requestURI = RecordingConfig.XIVO_REST_SERVICE_ROOT_PATH + \
                    RecordingConfig.XIVO_RECORDING_SERVICE_PATH + "/"
    param_str = "?activated=true&queue_name=%s" % queue_name

    requestURI += param_str

    headers = RecordingConfig.CTI_REST_DEFAULT_CONTENT_TYPE

    connection.request("GET", requestURI, None, headers)

    reply = connection.getresponse()

    if (reply.status != "200"):
        raise RestAPIError()

    return reply.read()


def extract_campaign_details(campaign_json):
    if (len(campaign_json) == 0):
        return None
    campaign = rest_encoder.decode(campaign_json)
    return campaign[0]


def _init_logging(debug_mode):
    global logger
    logger = logging.getLogger()
    formatter = logging.Formatter('%%(asctime)s [%%(process)d] (%%(levelname)s) (%%(name)s): %%(message)s')
    if debug_mode:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logfilehandler = logging.FileHandler(LOGFILE)
    logfilehandler.setFormatter(formatter)
    logger.addHandler(logfilehandler)


def main():
    _init_logging(DEBUG_MODE)
    global agi
    agi = AGI()

    queue_name = get_variables()
    campaigns_json = None
    try:
        campaigns_json = get_campaigns(queue_name)
    except RestAPIError:
        logger.error("REST WS: GET campaigns error")
        sys.exit(REST_ERROR)

    try:
        campaign_details = extract_campaign_details(campaigns_json)
    except Exception:
        logger.error("REST WS: Parse JSON reply error")
        sys.exit(REST_ERROR)

    if (campaign_details['base_filename'] != None):
        agi.set_variable('QR_RECORDQUEUE', '1')
        agi.set_variable('QR_BASE_FILENAME', campaign_details['base_filename'])
        logger.info('Calls to queue: "' + queue_name + '" are recorded')
        # event if create in the database fails, we record
        add_recording_detail(campaign_details)
    else:
        agi.set_variable('QR_RECORDQUEUE', '0')
        logger.info('Calls to queue: "' + queue_name + '" are not recorded')

    sys.exit(0)


if __name__ == '__main__':
    main()
