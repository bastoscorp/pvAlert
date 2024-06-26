import os
import time
from os.path import exists as file_exists

from config.config import Config
from business.connectManager import ConnectManager
from business.solarDevicesManager import SolarDevicesManager


conf = Config('../config.ini')
mgmt = ConnectManager(conf)

def test_init_device_manager_without_cache_info_file():
    file = conf.cacheInfoFile
    oldfilename = 'cache_info.txt.old'
    if file_exists(file):
        os.rename(file, oldfilename)
        time.sleep(2)
    l_dev = ""
    l_dev = SolarDevicesManager(mgmt)
    fex = file_exists(file)
    ret = False
    if(l_dev.station_code != "" and l_dev.inverter.device_id != "" and l_dev.inverter.device_name != ""
            and l_dev.ps.device_id != "" and l_dev.ps.device_name != "" and fex == True):
        ret = True
    if ret and file_exists(oldfilename):
        os.remove(oldfilename)
    else:
        os.rename(oldfilename,file)
    time.sleep(2)
    assert ret

def test_init_device_manager():
    l_dev = SolarDevicesManager(mgmt)
    if (l_dev.station_code == "" and l_dev.inverter.device_id == "" and l_dev.inverter.device_name == ""
            and l_dev.ps.device_id == "" and l_dev.ps.device_name == ""):
        assert False
    else:

        assert True


def test_init_device_manager_outdated_cache_info_file():
    l_dev = SolarDevicesManager(mgmt)
    old_cache_duration = conf.cacheInfoFileDuration
    test_cache_duration = 1
    conf.cacheInfoFileDuration = test_cache_duration
    ret = l_dev.load_station_and_devices_info()
    conf.cacheInfoFileDuration = old_cache_duration
    if not ret:
        assert True
    else:
        assert False

def test_get_station_with_wrong_url():
    good_station_url = conf.stationUri
    fake_station_url = "https://dummy.url/thirdData/stations"
    conf.stationUri = fake_station_url
    try:
        SolarDevicesManager(mgmt)
    except Exception as err:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(err).__name__, err.args)
        conf.stationUri = good_station_url
        assert True


def test_get_device_with_wrong_url():
    good_device_url = conf.devicesUri
    fake_device_url = "https://dummy.url/thirdData/getDevList"
    conf.devicesUri = fake_device_url
    try:
        dev = SolarDevicesManager(mgmt)
    except Exception as err:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(err).__name__, err.args)
        conf.devicesUri = good_device_url
        assert True

def test_get_inverter_data():
    l_dev = SolarDevicesManager(mgmt)
    l_dev.get_inverter_data()
    if l_dev.inverter.power == "" and l_dev.inverter.status == "":
        assert False
    else:
        assert True

def test_get_powersensor_data():
    l_dev = SolarDevicesManager(mgmt)
    l_dev.get_powersensor_data()
    if l_dev.ps.power == "" and l_dev.ps.status == "":
        assert False
    else:
        assert True


def test_get_inverter_data_with_wrong_url():
    good_url = conf.devicesUri
    fake_url = "https://dummy.url/thirdData/getDevRealKpi"
    conf.deviceKpiUri = fake_url
    dev = SolarDevicesManager(mgmt)
    try:
        dev.get_inverter_data()
    except Exception as err:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(err).__name__, err.args)
        conf.deviceKpiUri = good_url
        assert True


def test_get_powersensor_data_with_wrong_url():
    good_url = conf.devicesUri
    fake_url = "https://dummy.url/thirdData/getDevRealKpi"
    conf.deviceKpiUri = fake_url
    dev = SolarDevicesManager(mgmt)
    try:
        dev.get_powersensor_data()
    except Exception as err:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(err).__name__, err.args)
        conf.deviceKpiUri = good_url
        assert True

def test_get_inverter_data_frequency_exception():
    dev = SolarDevicesManager(mgmt)
    result = False
    i = 0
    while i < 5:
        try:
            dev.get_inverter_data()
            result = False
        except Exception as exp:
            result = True
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exp).__name__, exp.args)
            print(message)
            i = 5
        i += 1
    assert result



