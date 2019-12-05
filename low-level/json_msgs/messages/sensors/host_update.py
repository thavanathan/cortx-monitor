"""
 ****************************************************************************
 Filename:          host_update.py
 Description:       Defines the JSON message transmitted by the
                    node message handler. There may be a time when we need to
                    maintain state as far as messages being transmitted.  This
                    may involve aggregation of multiple messages before
                    transmissions or simply deferring an acknowledgment to
                    a later point in time.  For this reason, the JSON messages
                    are stored as objects which can be queued up, etc.
 Creation Date:     05/20/2015
 Author:            Jake Abernathy

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import json
import time
import calendar
from json_msgs.messages.sensors.base_sensors_msg import BaseSensorMsg
from framework.utils import mon_utils
class HostUpdateMsg(BaseSensorMsg):
    '''
    The JSON message transmitted by the node message handler
    '''

    ACTUATOR_MSG_TYPE = "host_update"
    MESSAGE_VERSION  = "1.0.0"

    ALERT_TYPE = "fault"
    SEVERITY = "warning"
    RESOURCE_TYPE = "node:os:system"
    RESOURCE_ID = "0"

    def __init__(self, host_id,
                       local_time,
                       boot_time,
                       up_time,
                       uname,
                       units,
                       site_id,
                       rack_id,
                       node_id,
                       cluster_id,
                       total_memory,
                       logged_in_users,
                       process_count,
                       running_process_count,
                       username  = "SSPL-LL",
                       signature = "N/A",
                       in_time      = "N/A",
                       expires   = -1):
        super(HostUpdateMsg, self).__init__()

        self._username          = username
        self._signature         = signature
        self._time              = in_time
        self._expires           = expires
        self._host_id           = host_id
        self._local_time        = local_time
        self._boot_time         = boot_time
        self._up_time           = up_time
        self._uname             = uname
        self._total_memory         = total_memory
        self._units             = units
        self._logged_in_users   = logged_in_users
        self._process_count     = process_count
        self._running_process_count = running_process_count
        self._site_id           = site_id
        self._rack_id           = rack_id
        self._node_id           = node_id
        self._cluster_id        = cluster_id

        epoch_time = str(int(time.time()))
        alert_id = mon_utils.get_alert_id(epoch_time)

        self._json = {
                      "username" : self._username,
                      "description" : self.DESCRIPTION,
                      "title" : self.TITLE,
                      "expires" : self._expires,
                      "signature" : self._signature,
                      "time" : epoch_time,

                      "message" : {
                          "sspl_ll_msg_header": {
                              "schema_version" : self.SCHEMA_VERSION,
                              "sspl_version"   : self.SSPL_VERSION,
                              "msg_version"    : self.MESSAGE_VERSION,
                              },
                          "sensor_response_type": {
                              "alert_type": self.ALERT_TYPE,
                              "severity": self.SEVERITY,
                              "alert_id": alert_id,
                              "host_id": self._host_id,
                              "info": {
                                "site_id": self._site_id,
                                "rack_id": self._rack_id,
                                "node_id": self._node_id,
                                "cluster_id": self._cluster_id,
                                "resource_type": self.RESOURCE_TYPE,
                                "resource_id": self.RESOURCE_ID,
                                "event_time": epoch_time
                              },
                              "specific_info": {
                                  "localtime" : self._local_time,
                                  "bootTime"  : self._boot_time,
                                  "upTime"    : self._up_time,
                                  "uname"     :  self._uname,
                                  "totalMemory" : self._total_memory,
                                  "loggedInUsers" : self._logged_in_users,
                                  "processCount"  : self._process_count,
                                  "runningProcessCount" : self._running_process_count
                                  }
                              }
                          }
                      }

    def getJson(self):
        """Return a validated JSON object"""
        # Validate the current message
        self.validateMsg(self._json)
        return json.dumps(self._json)
    def set_uuid(self, _uuid):
        self._json["message"]["sspl_ll_msg_header"]["uuid"] = _uuid
