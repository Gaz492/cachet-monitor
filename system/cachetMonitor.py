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

    httpErrors = {
        # Cloudflare Errors
        520: "Web server is returning an unknown error (Cloudflare)",
        521: "Web server is down (Cloudflare)",
        522: "Connection timed out (Cloudflare)",
        523: "Origin is unreachable (Cloudflare)",
        524: "A timeout occurred (Cloudflare)",
        525: "SSL handshake failed (Cloudflare)",
        526: "Invalid SSL certificate (Cloudflare)",
        # Nginx Errors
        444: "No Response (Nginx)",
        494: "Request Header Too Large (Nginx)",
        495: "Cert Error (Nginx)",
        496: "No Cert (Nginx)",
        497: "HTTP to HTTPS (Nginx)",
        499: "Client Closed Request (Nginx)",
        # Other
        # 1xx
        102: "Server has received and is processing the request",
        103: "resume aborted PUT or POST requests",
        122: "URI is longer than a maximum of 2083 characters",
        # 2xx
        207: "XML return with possible multiple seperate responses.",
        208: "The results are previously returned.",
        226: "The request has been fulfilled amd response is in instance manipulations.",
        # 3xx
        308: "Please connect again to the different URL using the same method.",
        # 4xx
        418: "I'm a teapot.",
        420: "Method Failure",
        421: "Enhance Your Calm",
        422: "Unprocessable Entity",
        423: "Locked",
        424: "Failed Dependency",
        426: "Upgrade Required",
        428: "Precondition Required",
        429: "Too Many Requests",
        431: "Request Header Fields Too Large",
        440: "Login Timeout (Microsoft)",
        449: "Retry With (Microsoft)",
        450: "Blocked by Windows Parental Controls",
        451: "Unavailable For Legal Reasons",
        # 5xx
        506: "Variant Also Negotiates (RFC 2295)",
        507: "Insufficient Storage (WebDAV; RFC 4918)",
        508: "Loop Detected (WebDAV; RFC 5842)",
        509: "Bandwidth Limit Exceeded (Apache bw/limited extension)",
        510: "Not Extended (RFC 2774)",
        511: "Network Authentication Required"

    }

    def __init__(self):
        self.logs = Logger()
        self.utils = Utils()
        self.config = self.utils.readConfig()
        self.base_url = self.config['api_url']
        self.api_token = self.config['api_token']
        self.maxRetries = self.config['retries']

        self.checkSites()

    def checkSites(self):
        # Count how many sites to monitor
        monitor_count = len(self.config['monitoring'])
        x = 0

        # Loop through sites to monitor
        while x < monitor_count:

            isEnabled = self.config['monitoring'][x]['enabled']
            status_codes = self.config['monitoring'][x]['expected_status_code']
            url = self.config['monitoring'][x]['url']
            request_method = self.config['monitoring'][x]['method']
            c_id = self.config['monitoring'][x]['component_id']
            localtime = time.asctime(time.localtime(time.time()))
            # current_status = self.getCurrentStatus(c_id)

            try:
                if isEnabled:
                    if request_method.lower() == "get":
                        r = requests.get(url, verify=True)
                        if r.status_code not in status_codes and r.status_code not in self.httpErrors:
                            self.logs.debug(httplib.responses[r.status_code])
                        elif r.status_code not in status_codes and r.status_code in self.httpErrors:
                            self.logs.debug(self.httpErrors[r.status_code])
                        self.logs.debug(url + " " + str(r.status_code))
                    elif request_method.lower() == "post":
                        requests.get(url, verify=True)
            except requests.exceptions.HTTPError as e:
                self.logs.info("HTTP Error: " + str(e))
            except requests.exceptions.SSLError as e:
                self.logs.info("SSL Error: " + str(e))
            except requests.exceptions.ConnectionError as e:
                self.logs.info("Connection Error: " + str(e))
            except requests.exceptions.Timeout as e:
                self.logs.info("Request Timeout: " + str(e))
            except requests.exceptions.TooManyRedirects as e:
                self.logs.info("Too many redirects: " + str(e))
            except requests.exceptions.RetryError as e:
                self.logs.info("Retry Error: " + str(e))
            except Exception as e:
                self.logs.info("Unexpected Error: " + str(e))

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

