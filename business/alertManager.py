from config.config import Config

import logging
import requests


class AlertManager:
    config: Config = None

    def __init__(self, conf: Config):
        self.config = conf

    def send_alert(self, message):
        url = self.config.alert_configured_url

        headers = {
            "Title": self.config.alert_title,
            "Tags": "warning"
        }

        response = requests.post(url, headers=headers, data=message.encode(encoding='utf-8'))

        if response.status_code == 200:
            logging.info("message sent!")
            return True
        else:
            logging.error("cannot send alert")
            return False
