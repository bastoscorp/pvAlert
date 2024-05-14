import logging

import requests

from config.config import Config

from controller.connectManager import ConnectManager

#res = requests.get('https://scotch.io')

#print(res)

# logging.basicConfig(level=logging.INFO,filename = 'datacamp.log')

logging.basicConfig(level=logging.INFO)

config = Config("config.ini")

logging.info(config.userName)
logging.info(config.baseUrl)
logging.info(config.loginUri)
logging.info(config.logoutUri)
logging.info(config.stationUri)
logging.info(config.devicesUri)
logging.info(config.deviceKpiUri)

mgmt = ConnectManager(config)
mgmt.init_session()

print(mgmt.session_cookie)