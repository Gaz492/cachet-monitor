#!/usr/bin/python
# coding=utf-8
import requests
import urllib3
import certifi
import httplib
import json

from utils import Utils



class Cachet(object):
    def __init__(self):
        self.utils = Utils()
        self.base_url = self.utils.readConfig()['api_url']
        self.api_token = self.utils.readConfig()['api_token']
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        self.checkSites()

    def checkForIncident(self, component_id):
        current_incidents = self.utils.getIncidents()
        incidents = len(current_incidents.json()['data'])
        x = 0

        while x < incidents:
            incident_id = current_incidents.json()['data'][x]['id']
            incident_component_id = current_incidents.json()['data'][x]['component_id']
            incident_status = current_incidents.json()['data'][x]['status']

            print(incident_id)
            print(incident_component_id)
            print(incident_status)

            if component_id == incident_component_id:
                return incident_id, incident_status
            x += 1


    def checkSites(self):
        # Count how many sites to monitor
        monitor_count = len(self.utils.readConfig()['monitoring'])
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
            status_codes = self.utils.readConfig()['monitoring'][x]['expected_status_code']
            url = self.utils.readConfig()['monitoring'][x]['url']
            c_id = self.utils.readConfig()['monitoring'][x]['component_id']
            try:
                r = self.http.request('GET', url, timeout=self.utils.readConfig()['monitoring'][x]['timeout'])
            except urllib3.exceptions.SSLError as e:
                print e
            except urllib3.exceptions.HTTPError as e:
                print e
            else:
                if r.status not in status_codes and r.status not in cfErrors:
                    print url
                    error_code = '%s HTTP Error %s: %s' % (url, r.status, httplib.responses[r.status])
                    print error_code
                    self.utils.putComponentsByID(c_id, status=4)
                elif r.status in cfErrors and r.status not in status_codes:
                    error_code = '%s HTTP Error %s: %s' % (url, r.status, cfErrors[r.status])
                    print error_code
                    self.utils.putComponentsByID(c_id, status=4)
                elif r.status in status_codes:
                    try:
                        current_status = self.utils.getComponentsByID(c_id).json()['data']['status']
                        if current_status not in status_codes:
                            print('component id: %s' % c_id)
                            self.utils.putComponentsByID(c_id, status=1)
                            incident_id, incident_status = self.checkForIncident(c_id)

                            if incident_id and incident_status:
                                print "active incident"
                    except requests.exceptions.SSLError as e:
                        print(e)
            x += 1
Cachet()
