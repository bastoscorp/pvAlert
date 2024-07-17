import ipaddress
from os.path import exists as file_exists

from config.config import Config
from business.actionDevicePhilipsHue import ActionDevicePhilipsHue


conf = Config('../config.ini')
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

def test_get_device_id():
    hue_id = adm_hue.get_device_id("PAC piscine")
    assert hue_id != None


def test_get_device_id_KO():
    hue_id = adm_hue.get_device_id("azerzrtzretzertezrt")
    assert hue_id == None

def test_get_device_status():
    status = adm_hue.get_device_status("PAC piscine")
    assert status != None

def test_enable_plug():
    if adm_hue.enable_plug("PAC piscine"):
        status = adm_hue.get_device_status("PAC piscine")
        assert status['status'] == True
    else:
        assert False
def test_disable_plug():
    if adm_hue.disable_plug("PAC piscine"):
        status = adm_hue.get_device_status("PAC piscine")
        assert status['status'] == False
    else:
        assert False
