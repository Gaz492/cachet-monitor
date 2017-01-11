#!/usr/bin/python
# coding=utf-8
import requests
import urllib3
import certifi
import httplib

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
                r = self.http.request('GET', url, retries=False, timeout=self.utils.readConfig()['monitoring'][x]['timeout'])
            except urllib3.exceptions.SSLError as e:
                print e
            except urllib3.exceptions.MaxRetryError as e:
                print e
            except urllib3.exceptions.NewConnectionError as e:
                print e
            except urllib3.exceptions.HTTPError as e:
                print e
            else:
                if r.status not in status_codes and r.status not in cfErrors:
                    error_code = '%s HTTP Error %s: %s' % (url, r.status, httplib.responses[r.status])
                    self.utils.putComponentsByID(c_id, status=4)
                    self.__reportIncident('%s: HTTP Error' % url, error_code, 2, 1, 5, 1)
                elif r.status in cfErrors and r.status not in status_codes:
                    error_code = '%s HTTP Error %s: %s' % (url, r.status, cfErrors[r.status])
                    self.__reportIncident('%s: HTTP Error' % url, error_code, 2, 1, 5, 1)
                    self.utils.putComponentsByID(c_id, status=4)
                elif r.status in status_codes:
                    current_status = self.utils.getComponentsByID(c_id).json()['data']['status']
                    if current_status not in status_codes:
                        print('component id: %s' % c_id)
                        self.utils.putComponentsByID(c_id, status=1)
                        # incident_id, incident_status = self.checkForIncident(c_id)
                        #
                        # if incident_id and incident_status:
                        #     print "active incident"
            x += 1

    def __reportIncident(self, title, description, status, visible, c_id, c_status):
        print("Title: %s, Description: %s, Status: %s, Visible: %s, Component ID: %s, Component Status: %s" % (title, description, str(status), str(visible), str(c_id), str(c_status)))

    def __updateIncident(self, i_id, description, status, c_status):
        print("Incident ID: %s, Description: %s, Status: %s, Component Status: %s" % (i_id, description, status, c_status))

Cachet()
