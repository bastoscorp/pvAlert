from config.config import Config

conf = Config('../data/config_test.ini')
def test_config_userName():
    assert conf.userName == "theUser"

def test_config_password():
    assert conf.systemCode == "pwd"

def test_config_domain():
    assert conf.baseUrl == "https://domain/thirdData/"

def test_config_login():
    assert conf.loginUri == "https://domain/thirdData/login"

def test_config_logout():
    assert conf.logoutUri == "https://domain/thirdData/logout"

def test_config_stations():
    assert conf.stationUri == "https://domain/thirdData/stations"

def test_config_devices():
    assert conf.devicesUri == "https://domain/thirdData/getDevList"

def test_config_devicesKpi():
    assert conf.deviceKpiUri == "https://domain/thirdData/getDevRealKpi"