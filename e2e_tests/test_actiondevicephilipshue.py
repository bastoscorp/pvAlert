import ipaddress
import os
from os.path import exists as file_exists

import sys
sys.path.insert(0, '../pvAlert')

from config.config import Config
from business.actionDevicePhilipsHue import ActionDevicePhilipsHue

# should have a configured philips hue tor testing

dirname = os.path.dirname(__file__)
#get parrent config file
home = os.path.dirname(dirname)
conffile = os.path.join(home, 'config.ini')
conf = Config(conffile)
adm_hue = ActionDevicePhilipsHue(conf)

def test_save_cache():
    if adm_hue.bridge_ip != None:
        adm_hue.save_cache_data()
        file = conf.hue_cache_file
        assert file_exists(file)
    else:
        assert False

def test_load_cache():
    adm_hue.bridge_ip = None
    adm_hue.load_cache_data()
    # test if it is an v4 ip address
    assert ipaddress.ip_address(adm_hue.bridge_ip)

def test_bridge_ip_discovery():
    adm_hue.bridge_ip = None
    adm_hue.discover_ip()
    # test if it is an v4 ip address
    assert ipaddress.ip_address(adm_hue.bridge_ip)


def test_get_device_id_KO():
    hue_id = adm_hue.get_device_id("azerzrtzretzertezrt")
    assert hue_id == None


