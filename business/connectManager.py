import base64
import json
import logging
import pickle
import time
import os
import requests

from os.path import exists as file_exists
import os.path

from config.config import Config



class ConnectManager:
    session_cookie = {}
    config: Config = None
    contentType = {}

    def __init__(self, conf: Config):
        """
        :rtype: object
        """
        self.config = conf
        self.contentType["Content-Type"] = "application/json"

    def init_session(self):
        if not self.load_session():
            self.login()

    def decode_pwd(self, encoded):
        decoded_bytes = base64.b64decode(encoded)
        decoded_string = decoded_bytes.decode("utf-8").rstrip()
        return decoded_string

    def login(self):
        uri = self.config.loginUri
        data = {"userName": self.config.userName, "systemCode": self.decode_pwd(self.config.systemCode)}
        json_data = json.dumps(data)
        try:
            response = requests.post(uri, data=json_data)
            rep_data = response.json()
            if rep_data['success']:
                ck = response.cookies
                self.session_cookie["XSRF-TOKEN"] = ck.get("XSRF-TOKEN")
                self.save_session()
        except requests.exceptions.HTTPError as err:
            logging.error("Error HTTP:", err)
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
            raise SystemExit(errc)

    def save_session(self):
        session_file = self.config.sessionFile
        with open(session_file, 'wb') as f1:
            pickle.dump(self.session_cookie, f1)

    def load_session(self):
        session_file = self.config.sessionFile
        ret = False
        if file_exists(session_file):
            with open(session_file, 'rb') as f1:
                session = pickle.load(f1)
            # if session is older than 30 min --> need to delete it and create another
            c_timestamp = os.path.getctime(session_file)
            session_duration = self.config.sessionDuration
            age = (time.time() - c_timestamp)
            if age < session_duration:
                self.session_cookie = session
                ret = True
            else:
                self.logout(session)
        logging.debug("ret value : ", ret)
        return ret

    def delete_session(self):
        self.session_cookie = {}
        os.remove(self.config.sessionFile)
        if os.path.exists(self.config.sessionFile):
            return False
        else:
            return True

    def logout(self, session):
        logout_uri = self.config.logoutUri
        header = self.contentType
        header["XSRF-TOKEN"] = session["XSRF-TOKEN"]
        json_data = json.dumps(header)
        try:
            response = requests.post(logout_uri, data=json_data)
            if response.status_code == 200:
                self.delete_session()
        except requests.exceptions.HTTPError as err:
            logging.error("Error HTTP:", err)
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
            raise SystemExit(errc)
