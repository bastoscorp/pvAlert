import configparser
import os
from urllib.parse import urljoin


class Config:
    baseUrl = ''
    userName = ''
    systemCode = ''
    sessionFile = ''
    sessionDuration: int = 0

    loginUri = ''
    logoutUri = ''
    stationUri = ''
    cacheInfoFile = ''
    cacheInfoFileDuration: int = 0
    devicesUri = ''
    deviceKpiUri = ''

    hue_discovery_url = ''
    hue_url_all_dev = ''
    hue_username = ''
    hue_client_key = ''
    hue_cache_file = ''
    hue_cache_duration: int = 0

    alert_title = ""
    alert_configured_url = ""

    def __init__(self, file: str):
        """

        :rtype: Config object with all vars
        """
        config = configparser.ConfigParser()
        config.read(file)

        config_dir = os.path.dirname(__file__)
        pv_home = os.path.dirname(config_dir)

        self.baseUrl = config.get('General', 'domain')
        self.userName = config.get('General', 'user')
        self.systemCode = config.get('General', 'password')

        sess_file = config.get('Session', 'connectionFile')
        self.sessionFile = os.path.join(pv_home, sess_file)
        self.check_dirs(self.sessionFile)

        self.sessionDuration = int(config.get('Session', 'duration'))

        self.loginUri = urljoin(self.baseUrl, config.get('Login', 'urn'))
        self.logoutUri = urljoin(self.baseUrl, config.get('Logout', 'urn'))
        self.stationUri = urljoin(self.baseUrl, config.get('Station', 'urn'))

        station_info_file = config.get('Station', 'cacheInfoFile')
        self.cacheInfoFile = os.path.join(pv_home, station_info_file)
        self.check_dirs(self.cacheInfoFile)

        self.cacheInfoFileDuration = int(config.get('Station', 'duration'))
        self.devicesUri = urljoin(self.baseUrl, config.get('Devices', 'urn'))
        self.deviceKpiUri = urljoin(self.baseUrl, config.get('DevicesKpi', 'urn'))

        self.alert_configured_url = urljoin(config.get("alert", "url"), config.get("alert", "topic"))
        self.alert_title = config.get("alert", "title")

        self.hue_discovery_url = config.get("action_philips_hue", "discover_url")
        self.hue_url_all_dev = config.get("action_philips_hue", "bridge_all_light_devices")
        self.hue_username = config.get("action_philips_hue", "hue_username")
        self.hue_client_key = config.get("action_philips_hue", "hue_client_key")

        hue_cache = config.get("action_philips_hue", "cacheFile")
        self.hue_cache_file = os.path.join(pv_home, hue_cache)
        self.check_dirs(self.hue_cache_file)

        self.hue_cache_duration = int(config.get("action_philips_hue", "cache_duration"))

    @staticmethod
    def check_dirs(path):
        parent = os.path.dirname(path)
        if not (os.path.exists(parent)):
            os.makedirs(parent)
