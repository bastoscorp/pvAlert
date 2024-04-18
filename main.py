import requests
from config import config

res = requests.get('https://scotch.io')

print(res)


print(config.baseUrl)

