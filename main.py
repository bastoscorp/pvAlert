import logging

import requests

from config.config import Config

from business.connectManager import ConnectManager

from business.deviceManager import DeviceManager

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
devices = DeviceManager(mgmt)




devices.get_inverter_data()
devices.get_powersensor_data()

print("inverter power = ", devices.inverter.power)
print("inverter status = ", devices.inverter.status)

print("powersensor power = ", devices.ps.power)
print("powersensor status = ", devices.ps.status)

#devices.get_station_code()

#mgmt.init_session()


#print(mgmt.session_cookie)