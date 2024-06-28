import logging

from logging.handlers import TimedRotatingFileHandler
from config.config import Config
from business.rulesManager import RulesManager


console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s'))

import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'logs/pvAlerts.log')
print(filename)
file_handler = logging.FileHandler(filename)
file_handler.setFormatter(logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s'))
file_handler.handlers = TimedRotatingFileHandler('logs/pvAlerts.log', when='D', interval=30, encoding="utf-8")

logging.basicConfig(handlers=[console_handler, file_handler], level=logging.INFO)

#
logging.info("Start pvAlert Checking ....")


config = Config("config.ini")
conso_manager = RulesManager(config)
conso_manager.control_status()
conso_manager.control_rules()
