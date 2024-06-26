import configparser
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
    topic = ''
    title = ''

    hue_discovery_url = ''
    hue_url_all_dev = ''
    hue_username = ''
    hue_client_key = ''
    hue_cache_file = ''
    hue_cache_duration: int = 0

    def __init__(self, file: str) -> object:
        """

        :rtype: Config object with all vars
        """
        config = configparser.ConfigParser()
        config.read(file)
        self.baseUrl = config.get('General', 'domain')
        self.userName = config.get('General', 'user')
        self.systemCode = config.get('General', 'password')
        self.sessionFile = config.get('Session', 'connectionFile')
        self.sessionDuration = int(config.get('Session', 'duration'))

        self.loginUri = urljoin(self.baseUrl, config.get('Login', 'urn'))
        self.logoutUri = urljoin(self.baseUrl, config.get('Logout', 'urn'))
        self.stationUri = urljoin(self.baseUrl, config.get('Station', 'urn'))
        self.cacheInfoFile = config.get('Station', 'cacheInfoFile')
        self.cacheInfoFileDuration = int(config.get('Station', 'duration'))
        self.devicesUri = urljoin(self.baseUrl, config.get('Devices', 'urn'))
        self.deviceKpiUri = urljoin(self.baseUrl, config.get('DevicesKpi', 'urn'))

        self.hue_discovery_url = config.get("action_philips_hue","discover_url")
        self.hue_url_all_dev = config.get("action_philips_hue","bridge_all_light_devices")
        self.hue_username = config.get("action_philips_hue","hue_username")
        self.hue_client_key = config.get("action_philips_hue","hue_client_key")
        self.hue_cache_file = config.get("action_philips_hue","cacheFile")
        self.hue_cache_duration = int(config.get("action_philips_hue","cache_duration"))