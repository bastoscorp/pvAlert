import logging

from config.config import Config
from business.rulesManager import RulesManager


logging.basicConfig(level=logging.INFO)

config = Config("config.ini")


conso_manager = RulesManager(config)
conso_manager.control_status()
conso_manager.control_rules()
