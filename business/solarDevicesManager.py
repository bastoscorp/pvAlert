import json
import logging
import requests
import pickle
import os
import time

from os.path import exists as file_exists
from business.connectManager import ConnectManager
from business.inverterDevice import InverterDevice
from business.powersensorDevice import PowersensorDevice
from exception.HuaweiApiFrequencyException import HuaweiApiFrequencyException
from exception.HuaweiApiException import HuaweiApiException

class SolarDevicesManager:

    session_mgmt = ""
    station_code = ""
    inverter = InverterDevice()
    ps = PowersensorDevice()

    def __init__(self, mgmt: ConnectManager):
        self.session_mgmt = mgmt
        self.session_mgmt.init_session()
        self.init_station_and_devices()

    def init_station_and_devices(self):
        if not self.load_station_and_devices_info():
            self.save_station_and_devices_info()

    def load_station_and_devices_info(self):
        cache_info_file = self.session_mgmt.config.cacheInfoFile
        ret = False
        if file_exists(cache_info_file):
             with open(cache_info_file, 'rb') as f1:
                 #in case of cacheInfoFile is older than 24h --> need to delete it and create another
                 c_timestamp = os.path.getctime(cache_info_file)
                 duration = self.session_mgmt.config.cacheInfoFileDuration
                 age = (time.time() - c_timestamp)
                 if age < duration:
                    data = pickle.load(f1)
                    self.station_code = data['station_code']
                    self.inverter.device_id = data['inverter_device_id']
                    self.inverter.device_name = data['inverter_device_name']
                    self.ps.device_id = data['ps_device_id']
                    self.ps.device_name = data['ps_device_name']
                    ret = True
        logging.debug("ret value : ", ret)
        return ret

    def save_station_and_devices_info(self):
        if self.station_code == "" and self.inverter.device_id == "" and self.ps.device_id == "":
            self.get_station_code()
            self.get_devices()
        cache_info_file = self.session_mgmt.config.cacheInfoFile
        data = {'station_code': self.station_code,
                'inverter_device_id': self.inverter.device_id,
                'inverter_device_name': self.inverter.device_name,
                'ps_device_id': self.ps.device_id,
                'ps_device_name': self.ps.device_name}
        with open(cache_info_file, 'wb') as f1:
            pickle.dump(data, f1)

    def get_station_code(self):
        # max 24 calls per day
        uri = self.session_mgmt.config.stationUri
        headers = {"XSRF-TOKEN": self.session_mgmt.session_cookie["XSRF-TOKEN"], "Content-Type": self.session_mgmt.contentType["Content-Type"]}
        data = {"pageNo":1, "pageSize":100}
        json_data = json.dumps(data)
        try:
            response = requests.post(uri, headers=headers, data=json_data)
            rep_data = response.json()
            if rep_data['success']:
                data = rep_data["data"]
                lst = data["list"]
                self.station_code = lst[0]["plantCode"]
        except requests.exceptions.HTTPError as err:
            logging.error("Error HTTP:", err)
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
            raise SystemExit(errc)


    def get_devices(self):
        #max 24 calls per day
        uri = self.session_mgmt.config.devicesUri
        headers = {"XSRF-TOKEN": self.session_mgmt.session_cookie["XSRF-TOKEN"], "Content-Type": self.session_mgmt.contentType["Content-Type"]}
        data = {"stationCodes": self.station_code}
        json_data = json.dumps(data)
        try:
            response = requests.post(uri, headers=headers , data=json_data)
            rep_data = response.json()
            if rep_data['success']:
                data = rep_data["data"]
                for dev in data:
                    if dev["devTypeId"] == self.inverter.device_type_code:
                        self.inverter.device_id = dev["id"]
                        self.inverter.device_name = dev["devName"]
                    if dev["devTypeId"] == self.ps.device_type_code:
                        self.ps.device_id = dev["id"]
                        self.ps.device_name = dev["devName"]
            elif not rep_data["success"] and rep_data["failCode"] == 407:
                err = rep_data["data"]
                msg = "Query Frequency Too High"
                logging.error(msg, err)
                raise HuaweiApiFrequencyException(msg, err)
            else:
                raise HuaweiApiException("issue with Huawei API", rep_data)
        except requests.exceptions.HTTPError as err:
            logging.error("Error HTTP:", err)
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
            raise SystemExit(errc)

    def get_inverter_data(self):
        uri = self.session_mgmt.config.deviceKpiUri
        headers = {"XSRF-TOKEN": self.session_mgmt.session_cookie["XSRF-TOKEN"], "Content-Type": self.session_mgmt.contentType["Content-Type"]}
        data = {"devIds": self.inverter.device_id, "devTypeId": self.inverter.device_type_code}
        json_data = json.dumps(data)
        try:
            response = requests.post(uri, headers=headers , data=json_data)
            rep_data = response.json()
            if rep_data['success']:
                data = rep_data["data"][0]
                kpi = data["dataItemMap"]
                self.inverter.status = int(kpi["inverter_state"])
                self.inverter.power = kpi["active_power"]
                self.inverter.temperature = kpi["temperature"]
            elif not rep_data["success"] and rep_data["failCode"] == 407:
                err = rep_data["data"]
                msg = "Query Frequency Too High"
                logging.error(msg,err)
                raise HuaweiApiFrequencyException(msg, err)
            else:
                raise HuaweiApiException("issue with Huawei API", rep_data)
        except requests.exceptions.HTTPError as err:
            logging.error("Error HTTP:", err)
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
            raise SystemExit(errc)

    def get_powersensor_data(self):
        uri = self.session_mgmt.config.deviceKpiUri
        headers = {"XSRF-TOKEN": self.session_mgmt.session_cookie["XSRF-TOKEN"], "Content-Type": self.session_mgmt.contentType["Content-Type"]}
        data = {"devIds": self.ps.device_id, "devTypeId": self.ps.device_type_code}
        json_data = json.dumps(data)
        try:
            response = requests.post(uri, headers=headers , data=json_data)
            rep_data = response.json()
            if rep_data['success']:
                data = rep_data["data"][0]
                kpi = data["dataItemMap"]
                self.ps.status = kpi["meter_status"]
                self.ps.power = kpi["active_power"]
            elif not rep_data["success"] and rep_data["failCode"] == 407:
                err = rep_data["data"]
                msg = "Query Frequency Too High"
                logging.error(msg, err)
                raise HuaweiApiFrequencyException(msg, err)
            else:
                raise HuaweiApiException("issue with Huawei API", rep_data)
        except requests.exceptions.HTTPError as err:
            logging.error("Error HTTP:", err)
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
            raise SystemExit(errc)