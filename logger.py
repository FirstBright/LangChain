import os
import logging
from datetime import datetime
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)
logfile = 'log.txt'
class Logger():
    def log_message(self, messages):      
        try:
            with open(logfile, 'a') as f:
                f.write(f"{messages}")
            logging.info(f'Message successfully written to log.txt')
        except Exception as e:
            logging.error(f'Error {e}')

        