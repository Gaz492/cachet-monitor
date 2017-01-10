#!/usr/bin/python
# coding=utf-8
import urllib3
import certifi
import httplib
import json
from pprint import pprint

# Static vars

status_codes = [200, 201, 202, 203, 204, 205, 206, 208, 226]
x = 0

# Open Json File
with open('config.json', 'r') as json_data:
    data = json.load(json_data)

# Count how many sites to monitor
monitor_count = len(data['monitoring'])

pprint(data)

# Loop through sites to monitor
while (x < monitor_count):

    pprint(data['monitoring'][x]['url'])

    url = data['monitoring'][x]['url']

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    try:
        r = http.request('GET', url, timeout=data['monitoring'][x]['timeout'])
    except urllib3.exceptions.SSLError as e:
        print e
    except urllib3.exceptions.HTTPError as e:
        print e
    else:
        if r.status not in status_codes:
            print 'HTTP Error %s: %s' % (r.status, httplib.responses[r.status])
    x += 1
