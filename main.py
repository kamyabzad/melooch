import os
from pathlib import Path
import random
import json
import time

import dotenv
import schedule

from TelegramForwarder import TelegramForwarder

dotenv.load_dotenv()

json_config_path = os.path.join(Path(__file__).parent.absolute(), 'config.json')
with open(json_config_path) as file:
    config = json.load(file)
    
forwarder = TelegramForwarder('send-to-groups', os.getenv('API_ID'), os.getenv('API_HASH'), config)

def start_forwarding():
    schedule.every(config['TimeIntervalMinutes']).minutes.do(forwarder.forward_messages).tag('forwarding')
    
def stop_forwarding():
    schedule.clear('forwarding')
        
if config['StartOnRun']:
    start_forwarding()
else:
    schedule.every().day.at(config['StartTime']).do(start_forwarding)
    schedule.every().day.at(config['StopTime']).do(stop_forwarding)

while True:
    schedule.run_pending()
    time.sleep(1)
