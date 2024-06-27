from config.config import Config

conf = Config('../data/config_test.ini')
def test_config_userName():
    assert conf.userName == "Eugen_API"

def test_config_password():
    assert conf.systemCode == "SHVhd2VpQDIwMTk="

def test_config_domain():
    assert conf.baseUrl == "https://eu5.fusionsolar.huawei.com/thirdData/"

def test_config_session():
    assert conf.sessionFile == "../data/sessionFile.txt"

def test_config_session_duration():
    assert conf.sessionDuration == 1620

def test_config_login():
    assert conf.loginUri == "https://eu5.fusionsolar.huawei.com/thirdData/login"

def test_config_logout():
    assert conf.logoutUri == "https://eu5.fusionsolar.huawei.com/thirdData/logout"

def test_config_stations():
    assert conf.stationUri == "https://eu5.fusionsolar.huawei.com/thirdData/stations"

def test_config_station_cache_info_file():
    assert conf.cacheInfoFile == "../data/cache_info.txt"

def test_config_station_duration():
    assert conf.cacheInfoFileDuration == 86400

def test_config_devices():
    assert conf.devicesUri == "https://eu5.fusionsolar.huawei.com/thirdData/getDevList"

def test_config_devicesKpi():
    assert conf.deviceKpiUri == "https://eu5.fusionsolar.huawei.com/thirdData/getDevRealKpi"

def test_config_hue_discovery():
    assert conf.hue_discovery_url == "https://discovery.meethue.com"

def test_config_hue_all_dev():
    assert conf.hue_url_all_dev == "https://<bridge_ip>/clip/v2/resource/light"

def test_config_hue_username():
    assert conf.hue_username == "youpi"

def test_config_hue_client_key():
    assert conf.hue_client_key == "matin"

def test_config_hue_cache_file():
    assert conf.hue_cache_file == "philips_hue_cache.txt"

def test_config_hue_cache_file_duration():
    assert conf.hue_cache_duration == 86400

def test_config_alert_url_configured():
    assert conf.alert_configured_url == "https://ntfy.sh/a-Testing-topic"

def test_config_alert_title():
    assert conf.alert_title == "a title"