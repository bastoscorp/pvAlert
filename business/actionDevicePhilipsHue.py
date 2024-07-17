from config.config import Config
from os.path import exists as file_exists

import logging
import requests
import time
import os
import pickle
import json

import urllib3

urllib3.disable_warnings()


class ActionDevicePhilipsHue:
    config: Config = None
    bridge_ip: str = ''
    bridge_ip_token: str = "<bridge_ip>"

    def __init__(self, conf: Config):
        self.config = conf
        self.init_cache_data()

    def init_cache_data(self):
        if not self.load_cache_data():
            self.save_cache_data()

    def load_cache_data(self):
        cache_file = self.config.hue_cache_file
        ret = False
        if file_exists(cache_file):
            with open(cache_file, 'rb') as f1:
                # in case of cacheFile is older than 24h --> need to delete it and create another
                c_timestamp = os.path.getctime(cache_file)
                duration = self.config.hue_cache_duration
                age = (time.time() - c_timestamp)
                if age < duration:
                    data = pickle.load(f1)
                    self.bridge_ip = data['bridge_ip']
                    ret = True
        logging.debug("ret value : ", ret)
        return ret

    def save_cache_data(self):
        if self.bridge_ip is None:
            self.discover_ip()
        cache_file = self.config.hue_cache_file
        data = {'bridge_ip': self.bridge_ip
                }
        with open(cache_file, 'wb') as f1:
            pickle.dump(data, f1)

    def discover_ip(self):
        url_discovery = self.config.hue_discovery_url
        try:
            response = requests.get(url_discovery)
            if response.status_code == 200:
                rep_data = response.json()
                data = rep_data[0]
                self.bridge_ip = data['internalipaddress']
            else:
                logging.error(
                    "issue to get Philips Hue Bridge ip address, got http error : " + str(
                        response.status_code) + " reason : " + response.reason)
        except requests.exceptions:
            logging.error("issue to get Philips Hue Bridge ip address")

    def get_device_id(self, device_name):
        url_raw = self.config.hue_url_all_dev
        url = url_raw.replace(self.bridge_ip_token, self.bridge_ip)
        try:
            headers = {"hue-application-key": self.config.hue_username}
            response = requests.get(url, headers=headers, verify=False)
            target_id = ""
            if response.status_code == 200:
                rep_data = response.json()
                data = rep_data['data']
                data_size = len(data)
                i = 0
                while i < data_size:
                    dev = data[i]
                    metadata = dev['metadata']
                    name = metadata['name']
                    if name == device_name:
                        target_id = str(dev['id'])
                        i = data_size
                    i += 1
            else:

                logging.error("issue to reach Philips Hue Bridge, got http error : " + str(
                    response.status_code) + " reason : " + response.reason)

            if target_id != "":
                return target_id
            else:
                logging.error("cannot find device named :" + device_name)
                return None
        except requests.exceptions:
            logging.error("issue to reach Philips Hue bridge")
            return None

    def get_device_status(self, device_name):
        hue_id = self.get_device_id(device_name)
        status = None
        if hue_id is not None:
            url_raw = self.config.hue_url_all_dev
            url = url_raw.replace(self.bridge_ip_token, self.bridge_ip)
            url = url + '/' + hue_id
            headers = {"hue-application-key": self.config.hue_username}
            try:
                response = requests.get(url, headers=headers, verify=False)
                if response.status_code == 200:
                    rep_data = response.json()
                    data = rep_data['data']
                    status = data[0]["on"]["on"]
                else:
                    logging.error(
                        "issue to reach Philips Hue Bridge, got http error : " + str(
                            response.status_code) + " reason : " + response.reason)
            except requests.exceptions:
                logging.error("issue to reach Philips Hue bridge")
        else:
            logging.error("error to get this device id")
            raise Exception("issue to get " + device_name + " id")
        if status is True:
            data_to_return = {'status': True,
                              'message': "powered on"
                              }
            return data_to_return
        if status is False:
            data_to_return = {'status': False,
                              'message': "powered off"
                              }
            return data_to_return
        if status is None:
            return None

    def send_command(self, action, device_name):
        data = None
        ret = False
        if action == "enable":
            data = {
                "on": {
                    "on": True
                }
            }
        if action == "disable":
            data = {
                "on": {
                    "on": False
                }
            }
        if data is not None:
            hue_id = self.get_device_id(device_name)
            if hue_id is not None:
                url_raw = self.config.hue_url_all_dev
                url = url_raw.replace(self.bridge_ip_token, self.bridge_ip)
                url = url + '/' + hue_id
                headers = {"hue-application-key": self.config.hue_username}

                json_data = json.dumps(data)
                try:
                    response = requests.put(url, headers=headers, data=json_data, verify=False)
                    if response.status_code == 200:
                        rep_data = response.json()
                        data = rep_data['data']
                        tab = data[0]
                        rid = tab['rid']
                        if rid == hue_id:
                            ret = True
                    else:
                        logging.error(
                            "issue to reach Philips Hue Bridge, got http error : " + str(
                                response.status_code) + " reason : " + response.reason)

                except requests.exceptions:
                    logging.error("issue to reach Philips Hue bridge")
            else:
                logging.error("error to get this device id")
                raise Exception("issue to get " + device_name + " id")
        return ret

    def enable_plug(self, device_name):
        return self.send_command("enable", device_name)

    def disable_plug(self, device_name):
        return self.send_command("disable", device_name)
