import logging
import os
from logging.handlers import TimedRotatingFileHandler
from config.config import Config
from business.rulesManager import RulesManager


console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s'))


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'logs/pvAlerts.log')

file_handler = logging.FileHandler("my_handler")
file_handler.setFormatter(logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s'))
file_handler.handlers = TimedRotatingFileHandler(filename, when='D', interval=1, encoding="utf-8")

logging.basicConfig(handlers=[console_handler, file_handler], level=logging.INFO)

#
logging.info("Start pvAlert Checking ....")

conf_filename = os.path.join(dirname, "config.ini")

config = Config(conf_filename)
conso_manager = RulesManager(config)
conso_manager.control_status()
conso_manager.control_rules()
