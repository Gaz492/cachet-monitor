import os
import logging
import datetime

from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph.output import GraphvizOutput


graphviz = GraphvizOutput()
graphviz.output_file = ' filter_exclude.jpg'
graphviz.output_type = ' jpg'


from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.date import DateTrigger
from system.cachetMonitor import Cachet
from system.utils import Utils

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
with PyCallGraph(output=graphviz):
    if not os.path.exists("settings/config.json"):
        print("|! Couldn't find config.json!")
        print("|! rename the config.json.example to config.json and edit it as required.")
        print("|! After that, run the script again.")
        exit(1)

    utils = Utils()
    schedule_interval = utils.readConfig()['interval']
    use_schedule = utils.readConfig()['use_schedule']

    logging.basicConfig()

    scheduler = BlockingScheduler()
    scheduler.add_job(Cachet, trigger=DateTrigger(run_date=datetime.datetime.now()), id='initial')
    scheduler.add_job(Cachet, 'interval', seconds=schedule_interval, id='constant')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    if use_schedule:
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
                pass
    else:
        Cachet()
