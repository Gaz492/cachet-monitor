#!/usr/bin/python
# coding=utf-8

import requests
import certifi
import httplib
import time
from system.logging import Logger


from utils import Utils

'''
   Copyright 2017 Gareth Williams

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''


class Cachet(object):

    def __init__(self):
        self.utils = Utils()
        self.config = self.utils.readConfig()
        self.base_url = self.config['api_url']
        self.api_token = self.config['api_token']
        self.maxRetries = self.config['retries']

        self.logs = Logger

        self.checkSites()

    def checkSites(self):
        # Count how many sites to monitor
        monitor_count = len(self.config['monitoring'])
        x = 0

        cfErrors = {
            520: "Web server is returning an unknown error",
            521: "Web server is down",
            522: "Connection timed out",
            523: "Origin is unreachable",
            524: "A timeout occurred",
            525: "SSL handshake failed",
            526: "Invalid SSL certificate"
        }

        # Loop through sites to monitor
        while x < monitor_count:
            isEnabled = self.config['monitoring'][x]['enabled']
            status_codes = self.config['monitoring'][x]['expected_status_code']
            url = self.config['monitoring'][x]['url']
            request_method = self.config['monitoring'][x]['method']
            c_id = self.config['monitoring'][x]['component_id']
            localtime = time.asctime(time.localtime(time.time()))
            try:
                if isEnabled:
                    if request_method.lower == "get":
                        None
                    elif request_method.lower == "post":
                        None
            except:
                None

            x += 1

    def checkForIncident(self, component_id):
        current_incidents = self.utils.getIncidents().json()
        incidents = len(current_incidents['data'])
        x = 0

        while x < incidents:
            incident_id = current_incidents['data'][x]['id']
            incident_component_id = current_incidents['data'][x]['component_id']
            incident_status = current_incidents['data'][x]['status']

            if component_id == incident_component_id and incident_status is not 4:
                return incident_id
            x += 1

    def getIncidentInfo(self, i_id):
        incident = self.utils.getIncidentsByID(i_id).json()
        i_description = incident['data']['message']
        return i_description

    def getCurrentStatus(self, c_id):
        current_status = self.utils.getComponentsByID(c_id).json()['data']['status']
        return current_status

