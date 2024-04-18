import configparser

config = configparser.ConfigParser()
config.read('config.ini')

baseUrl = config.get('General', 'domain')