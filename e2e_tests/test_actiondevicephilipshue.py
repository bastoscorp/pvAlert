import ipaddress
import os
import e2e_test_locator

from os.path import exists as file_exists
from config.config import Config
from business.actionDevicePhilipsHue import ActionDevicePhilipsHue


e2e_test_locator = e2e_test_locator
# should have a configured philips hue tor testing

current_dir = os.path.dirname(__file__)
# get parrent config file
home = os.path.dirname(current_dir)
conf_file = os.path.join(home, 'config.ini')
conf = Config(conf_file)
adm_hue = ActionDevicePhilipsHue(conf)


def test_save_cache():
    if adm_hue.bridge_ip is not None:
        adm_hue.save_cache_data()
        file = conf.hue_cache_file
        assert file_exists(file)
    else:
        assert False


def test_load_cache():
    adm_hue.bridge_ip = ''
    adm_hue.load_cache_data()
    # test if it is an v4 ip address
    assert ipaddress.ip_address(adm_hue.bridge_ip)


def test_bridge_ip_discovery():
    adm_hue.bridge_ip = ''
    adm_hue.discover_ip()
    # test if it is an v4 ip address
    assert ipaddress.ip_address(adm_hue.bridge_ip)


def test_get_device_id_ko():
    hue_id = adm_hue.get_device_id("azerzrtzretzertezrt")
    assert hue_id is None
