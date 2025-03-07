import time
import os
import e2e_test_locator

from config.config import Config
from business.connectManager import ConnectManager
from business.rulesManager import RulesManager


e2e_test_locator = e2e_test_locator

# need a configured config.ini file !!!

dirname = os.path.dirname(__file__)
# get parrent config file
home = os.path.dirname(dirname)
conffile = os.path.join(home, 'config.ini')
conf = Config(conffile)

mgmt = ConnectManager(conf)
my_rm = RulesManager(conf)


def test_refresh_data_timeout():
    my_rm.last_update = (time.time() - 605)
    my_rm.refresh_data()
    if my_rm.last_update is not None:
        assert True
    else:
        assert False


def test_refresh_data_intime():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.refresh_data()
    if my_rm.last_update == my_time:
        assert True
    else:
        assert False


def test_control_status_ok_case():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.inverter.status = 512
    my_rm.dev_mgmt.ps.status = 1
    assert my_rm.control_status()


def test_control_status_both_none_case():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.inverter.status = None
    my_rm.dev_mgmt.ps.status = None
    assert my_rm.control_status()


def test_control_status_one_ok_and_none_case():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.inverter.status = 512
    my_rm.dev_mgmt.ps.status = None
    assert my_rm.control_status()


def test_control_status_one_ko_and_none_case_other():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.inverter.status = None
    my_rm.dev_mgmt.ps.status = 0
    assert my_rm.control_status()


def test_control_status_both_ko():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.inverter.status = 768
    my_rm.dev_mgmt.ps.status = 0
    assert my_rm.control_status()


def test_control_status_one_ko_and_inverter_warning():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.inverter.status = 771
    my_rm.dev_mgmt.ps.status = 0
    assert my_rm.control_status()


def test_control_status_one_ok_and_inverter_warning():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.inverter.status = 771
    my_rm.dev_mgmt.ps.status = 1
    assert my_rm.control_status()


def test_control_status_one_ok_and_inverter_unknowned_code():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.inverter.status = 9999
    my_rm.dev_mgmt.ps.status = 1
    assert my_rm.control_status()


def test_control_rules_case_remaining_ok_for_one_device_when_devs_off():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.ps.power = 1500
    my_test_rules = [{'rule_id': 1,
                      'rule_name': "Pool Heating Threshold",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1000,
                      'rule_priority': 1,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev1',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 2,
                      'rule_name': "Water eater",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1500,
                      'rule_priority': 3,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev2',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 3,
                      'rule_name': "Water eater 2",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1500,
                      'rule_priority': 2,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev3',
                      'action_device_type': 'testing'
                      },
                     ]
    my_rm.power_rules.rules = my_test_rules

    status_off = {'status': False,
                  'message': "powered off"
                  }

    # status_on = {'status': True,
    #          'message': "powered on"
    #          }

    my_rm.action_devices_mgmt.testing_status["dev1"] = status_off
    my_rm.action_devices_mgmt.testing_status["dev2"] = status_off
    my_rm.action_devices_mgmt.testing_status["dev3"] = status_off

    my_rm.control_rules()
    dev1 = my_rm.action_devices_mgmt.get_device_status("testing", "dev1")
    dev1_status = dev1["status"]
    dev2 = my_rm.action_devices_mgmt.get_device_status("testing", "dev2")
    dev2_status = dev2["status"]
    dev3 = my_rm.action_devices_mgmt.get_device_status("testing", "dev3")
    dev3_status = dev3["status"]
    if dev1_status is True and dev2_status is False and dev3_status is False:
        assert True
    else:
        assert False


def test_control_rules_case_remaining_ok_for_x_devices_when_devs_off():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.ps.power = 1500
    my_test_rules = [{'rule_id': 1,
                      'rule_name': "Pool Heating Threshold",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1000,
                      'rule_priority': 1,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev1',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 2,
                      'rule_name': "Water eater",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 500,
                      'rule_priority': 3,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev2',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 3,
                      'rule_name': "Water eater 2",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1500,
                      'rule_priority': 2,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev3',
                      'action_device_type': 'testing'
                      },
                     ]
    my_rm.power_rules.rules = my_test_rules

    status_off = {'status': False,
                  'message': "powered off"
                  }

    # status_on = {'status': True,
    #          'message': "powered on"
    #          }

    my_rm.action_devices_mgmt.testing_status["dev1"] = status_off
    my_rm.action_devices_mgmt.testing_status["dev2"] = status_off
    my_rm.action_devices_mgmt.testing_status["dev3"] = status_off

    my_rm.control_rules()
    dev1 = my_rm.action_devices_mgmt.get_device_status("testing", "dev1")
    dev1_status = dev1["status"]
    dev2 = my_rm.action_devices_mgmt.get_device_status("testing", "dev2")
    dev2_status = dev2["status"]
    dev3 = my_rm.action_devices_mgmt.get_device_status("testing", "dev3")
    dev3_status = dev3["status"]
    if dev1_status is True and dev2_status is True and dev3_status is False:
        assert True
    else:
        assert False


def test_control_rules_case_remaining_ok_with_several_dev_on():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.ps.power = 1500
    my_test_rules = [{'rule_id': 1,
                      'rule_name': "Pool Heating Threshold",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1000,
                      'rule_priority': 1,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev1',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 2,
                      'rule_name': "Water eater",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 500,
                      'rule_priority': 3,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev2',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 3,
                      'rule_name': "Water eater 2",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1500,
                      'rule_priority': 2,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev3',
                      'action_device_type': 'testing'
                      },
                     ]
    my_rm.power_rules.rules = my_test_rules

    status_off = {'status': False,
                  'message': "powered off"
                  }

    status_on = {'status': True,
                 'message': "powered on"
                 }

    # prio 1:
    my_rm.action_devices_mgmt.testing_status["dev1"] = status_on
    # prio 3:
    my_rm.action_devices_mgmt.testing_status["dev2"] = status_on
    # prio 2:
    my_rm.action_devices_mgmt.testing_status["dev3"] = status_off

    my_rm.control_rules()
    dev1 = my_rm.action_devices_mgmt.get_device_status("testing", "dev1")
    dev1_status = dev1["status"]
    dev2 = my_rm.action_devices_mgmt.get_device_status("testing", "dev2")
    dev2_status = dev2["status"]
    dev3 = my_rm.action_devices_mgmt.get_device_status("testing", "dev3")
    dev3_status = dev3["status"]
    if dev1_status is True and dev2_status is True and dev3_status is True:
        assert True
    else:
        assert False


def test_control_rules_case_remaining_ok_when_on():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.ps.power = 1500
    my_test_rules = [{'rule_id': 1,
                      'rule_name': "Pool Heating Threshold",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1000,
                      'rule_priority': 1,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev1',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 2,
                      'rule_name': "Water eater",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 500,
                      'rule_priority': 3,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev2',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 3,
                      'rule_name': "Water eater 2",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1500,
                      'rule_priority': 2,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev3',
                      'action_device_type': 'testing'
                      },
                     ]
    my_rm.power_rules.rules = my_test_rules

    status_off = {'status': False,
                  'message': "powered off"
                  }

    status_on = {'status': True,
                 'message': "powered on"
                 }

    # prio 1:
    my_rm.action_devices_mgmt.testing_status["dev1"] = status_on
    # prio 3:
    my_rm.action_devices_mgmt.testing_status["dev2"] = status_off
    # prio 2:
    my_rm.action_devices_mgmt.testing_status["dev3"] = status_off

    my_rm.control_rules()
    dev1 = my_rm.action_devices_mgmt.get_device_status("testing", "dev1")
    dev1_status = dev1["status"]
    dev2 = my_rm.action_devices_mgmt.get_device_status("testing", "dev2")
    dev2_status = dev2["status"]
    dev3 = my_rm.action_devices_mgmt.get_device_status("testing", "dev3")
    dev3_status = dev3["status"]
    if dev1_status is True and dev2_status is False and dev3_status is True:
        assert True
    else:
        assert False


def test_control_rules_case_remaining_is_none():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.ps.power = None
    my_test_rules = [{'rule_id': 1,
                      'rule_name': "Pool Heating Threshold",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1000,
                      'rule_priority': 1,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev1',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 2,
                      'rule_name': "Water eater",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 500,
                      'rule_priority': 3,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev2',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 3,
                      'rule_name': "Water eater 2",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1500,
                      'rule_priority': 2,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev3',
                      'action_device_type': 'testing'
                      },
                     ]
    my_rm.power_rules.rules = my_test_rules

    my_rm.control_rules()
    dev1 = my_rm.action_devices_mgmt.get_device_status("testing", "dev1")
    dev1_status = dev1["status"]
    dev2 = my_rm.action_devices_mgmt.get_device_status("testing", "dev2")
    dev2_status = dev2["status"]
    dev3 = my_rm.action_devices_mgmt.get_device_status("testing", "dev3")
    dev3_status = dev3["status"]
    if dev1_status is False and dev2_status is False and dev3_status is False:
        assert True
    else:
        assert False


def test_control_rules_case_remaining_is_negative():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.ps.power = -186.0
    my_test_rules = [{'rule_id': 1,
                      'rule_name': "Pool Heating Threshold",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1000,
                      'rule_priority': 1,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev1',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 2,
                      'rule_name': "Water eater",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 500,
                      'rule_priority': 3,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev2',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 3,
                      'rule_name': "Water eater 2",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1500,
                      'rule_priority': 2,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev3',
                      'action_device_type': 'testing'
                      },
                     ]
    my_rm.power_rules.rules = my_test_rules

    status_on = {'status': True,
                 'message': "powered on"
                 }

    # prio 1:
    my_rm.action_devices_mgmt.testing_status["dev1"] = status_on
    # prio 3:
    my_rm.action_devices_mgmt.testing_status["dev2"] = status_on
    # prio 2:
    my_rm.action_devices_mgmt.testing_status["dev3"] = status_on

    my_rm.control_rules()
    dev1 = my_rm.action_devices_mgmt.get_device_status("testing", "dev1")
    dev1_status = dev1["status"]
    dev2 = my_rm.action_devices_mgmt.get_device_status("testing", "dev2")
    dev2_status = dev2["status"]
    dev3 = my_rm.action_devices_mgmt.get_device_status("testing", "dev3")
    dev3_status = dev3["status"]
    if dev1_status is False and dev2_status is False and dev3_status is False:
        assert True
    else:
        assert False


def test_control_rules_case_remaining_low_when_on():
    my_time = (time.time() - 60)
    my_rm.last_update = my_time
    my_rm.dev_mgmt.ps.power = 100
    my_test_rules = [{'rule_id': 1,
                      'rule_name': "Pool Heating Threshold",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1000,
                      'rule_priority': 1,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev1',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 2,
                      'rule_name': "Water eater",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 500,
                      'rule_priority': 3,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev2',
                      'action_device_type': 'testing'
                      },
                     {'rule_id': 3,
                      'rule_name': "Water eater 2",
                      'rule_type': "threshold",
                      'rule_remaining_power_value': 1500,
                      'rule_priority': 2,
                      'action_threshold_crossed': 'enable',
                      'action_device_name': 'dev3',
                      'action_device_type': 'testing'
                      },
                     ]
    my_rm.power_rules.rules = my_test_rules

    status_off = {'status': False,
                  'message': "powered off"
                  }

    status_on = {'status': True,
                 'message': "powered on"
                 }

    # prio 1:
    my_rm.action_devices_mgmt.testing_status["dev1"] = status_on
    # prio 3:
    my_rm.action_devices_mgmt.testing_status["dev2"] = status_off
    # prio 2:
    my_rm.action_devices_mgmt.testing_status["dev3"] = status_off

    my_rm.control_rules()
    dev1 = my_rm.action_devices_mgmt.get_device_status("testing", "dev1")
    dev1_status = dev1["status"]
    dev2 = my_rm.action_devices_mgmt.get_device_status("testing", "dev2")
    dev2_status = dev2["status"]
    dev3 = my_rm.action_devices_mgmt.get_device_status("testing", "dev3")
    dev3_status = dev3["status"]
    if dev1_status is True and dev2_status is False and dev3_status is False:
        assert True
    else:
        assert False
