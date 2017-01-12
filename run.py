import os
import logging
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.date import DateTrigger
from system.cachetMonitor import Cachet
from system.utils import Utils

utils = Utils()
schedule_interval = utils.readConfig()['interval']

logging.basicConfig()

if not os.path.exists("settings/config.json"):
    print "|! Couldn't find config.json!"
    print "|! rename the config.json.example to config.json and edit it as required."
    print "|! After that, run the script again."
    exit(1)

scheduler = BlockingScheduler()
scheduler.add_job(Cachet, trigger=DateTrigger(run_date=datetime.datetime.now()), id='initial')
scheduler.add_job(Cachet, 'interval', seconds=schedule_interval, id='constant')
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
        pass
