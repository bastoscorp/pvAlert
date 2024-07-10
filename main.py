import logging
import os
from logging.handlers import TimedRotatingFileHandler
from config.config import Config
from business.rulesManager import RulesManager

logging.root.setLevel(logging.INFO)

#formatter = logging.Formatter('%(asctime)s - %(module)s %(filename)s %(funcName)s:%(lineno)s - %(name)s -%(message)s')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)
console_handler.addFilter(logging.Filter())
logging.root.addHandler(console_handler)

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'logs/pvAlerts.log')

file_handler = logging.FileHandler(filename)
file_handler.setFormatter(formatter)
myTimeHandler = TimedRotatingFileHandler(filename, when='midnight', backupCount=60, encoding="utf-8")
myTimeHandler.suffix = "%Y-%m-%d.log"

file_handler.setLevel(logging.INFO)
file_handler.addFilter(logging.Filter())
logging.root.addHandler(file_handler)
logging.root.addHandler(myTimeHandler)


logging.info("Start pvAlert Checking ....")

conf_filename = os.path.join(dirname, "config.ini")

config = Config(conf_filename)
conso_manager = RulesManager(config)
conso_manager.control_status()
conso_manager.control_rules()
