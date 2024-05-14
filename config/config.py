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
    devicesUri = ''
    deviceKpiUri = ''
    
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
        self.devicesUri = urljoin(self.baseUrl, config.get('Devices', 'urn'))
        self.deviceKpiUri = urljoin(self.baseUrl, config.get('DevicesKpi', 'urn'))
