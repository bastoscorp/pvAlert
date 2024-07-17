import time
import pytest
import shutil

import os
from os.path import exists as file_exists
from shutil import copyfile

import sys
sys.path.insert(0, '../pvAlert')


from config.config import Config
from business.connectManager import ConnectManager


dirname = os.path.dirname(__file__)
#get parrent config file
home = os.path.dirname(dirname)
conffile = os.path.join(home, 'data/config_test.ini')
conf = Config(conffile)


mgmt = ConnectManager(conf)
current_session_file = conf.sessionFile + ".bak"

sessfile = os.path.join(home, 'data/sessionFile.txt')
copyfile(sessfile, conf.sessionFile)


def test_config_username():
    assert conf.userName == "Eugen_API"


@pytest.fixture
def manage_session_safe_delete_session_file():
    shutil.move(conf.sessionFile, current_session_file)
    if file_exists(current_session_file):
        assert True
    else:
        assert False
    yield
    shutil.move(current_session_file, conf.sessionFile)
    if file_exists(conf.sessionFile):
        assert True
    else:
        assert False


@pytest.fixture
def backup_restore_session_file():
    shutil.copy2(conf.sessionFile, current_session_file)
    if file_exists(current_session_file):
        assert True
    else:
        assert False
    yield
    shutil.move(current_session_file, conf.sessionFile)
    if file_exists(conf.sessionFile):
        assert True
    else:
        assert False


def test_save_and_load_session(manage_session_safe_delete_session_file):
    mgmt.session_cookie = "AAA111"
    mgmt.save_session()
    mgmt.session_cookie = ""
    mgmt.load_session()
    assert mgmt.session_cookie == "AAA111"


def test_delete_session(manage_session_safe_delete_session_file):
    mgmt.session_cookie = "AAA111"
    mgmt.save_session()
    mgmt.delete_session()
    assert mgmt.session_cookie == {}

def test_load_session_without_file(manage_session_safe_delete_session_file):
    ret = mgmt.load_session()
    if not ret:
        assert True
    else:
        assert False


def test_load_session_with_outdated_file(backup_restore_session_file):
    mgmt = ConnectManager(conf)
    old = conf.sessionDuration
    conf.sessionDuration = 1
    # await for file system to update
    time.sleep(2)
    ret = mgmt.load_session()
    conf.sessionDuration = old
    if not ret:
        assert True
    else:
        assert False


def test_logout_wrong_url():
    mgmt.load_session()
    good_url = conf.logoutUri
    fake_logout_url = "https://dummy.url/thirdData/logout"
    conf.logoutUri = fake_logout_url
    try:
        mgmt.logout(mgmt.session_cookie)
    except Exception as err:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(err).__name__, err.args)
        conf.logoutUri = good_url
        assert True

def test_login_with_wrong_credentials():
    mgmt.session_cookie = ""
    mgmt.login()
    if mgmt.session_cookie == "":
        assert True
    else:
        assert False


def test_login_with_wrong_url():
    mgmt.session_cookie = ""
    good_url = conf.loginUri
    fake_login_url = "https://dummy.url/thirdData/login"
    conf.loginUri = fake_login_url
    try:
        mgmt.login()
    except Exception as err:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(err).__name__, err.args)
        conf.loginUri = good_url
        assert True

