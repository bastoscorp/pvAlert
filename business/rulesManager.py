import logging
import time

from config.config import Config
from business.connectManager import ConnectManager
from business.solarDevicesManager import SolarDevicesManager
from business.inverterRules import InverterRules
from business.powersensorRules import PowersensorRules
from business.powerUsageRules import PowerUsageRules
from business.alertManager import AlertManager
from business.actionDeviceManager import ActionDeviceManager

class RulesManager:
    dev_mgmt: SolarDevicesManager = None
    last_update: time = None
    inverter_rules: InverterRules = InverterRules()
    ps_rules: PowersensorRules = PowersensorRules()
    power_rules: PowerUsageRules = PowerUsageRules()
    action_devices_mgmt: ActionDeviceManager = None
    alerter: AlertManager = None

    def __init__(self, conf: Config):
        self.dev_mgmt = SolarDevicesManager(ConnectManager(conf))
        self.alerter = AlertManager(conf)
        self.action_devices_mgmt = ActionDeviceManager(conf)
    def refresh_data(self):
        age = (time.time() - 600)
        my_timing = 1
        if self.last_update != None:
            my_timing = self.last_update
        if age > my_timing:
            self.dev_mgmt.get_inverter_data()
            self.dev_mgmt.get_powersensor_data()
            self.last_update = time.time()

    def control_status(self):
        messages = ""
        log_warning = ""
        self.refresh_data()
        status = False
        if self.dev_mgmt.inverter.status != None:
            # we got a status from Huawei ...
            str_statusCode = str(self.dev_mgmt.inverter.status)
            current_status = self.inverter_rules.status_list.get(str_statusCode)
            inverter_message = ""
            if current_status != None:
                #and ... we know the status
                status_inverter = True
                str_status = current_status["message"]
                message_type = current_status["type"]
                # need to alert ?
                if message_type != 'ok':
                    # error case:  log and alert
                    if message_type == 'error':
                        inverter_message = ("Inverter status KO, code : " + str(
                                            self.dev_mgmt.inverter.status) + " --> " + str_status + "\n"
                                            "Need manual action on AC/DC module as soon as possible\n")

                    #warning case: log but not alert
                    if message_type == 'warning':
                        logging.warning ("Inverter status different from OK ("+ str(self.inverter_rules.ok_status) +")")
                        logging.warning("Code received is : " + str_statusCode + " --> " + str_status)
                #good case here :
                else:
                    logging.info("Inverter OK")
            #unknown status here :
            else:
                inverter_message = ("Inverter unknowed status code : "+ str_statusCode +" \n")
                status_inverter = False
        # cannot get status here :
        else:
            inverter_message = ("Issue : impossible to get inverter status \n")
            status_inverter = False
        #stack messages
        if inverter_message != "":
            messages = messages + inverter_message + "\n"
        else:
            messages = ""

        if self.dev_mgmt.ps.status != None:
            status_ps = True
            if self.dev_mgmt.ps.status != self.ps_rules.ok_status:
                # need to alert
                ps_message = "Powersensor issue need manual action : check if powersensor is ON \n"
                messages = messages + ps_message
            else:
                logging.info("Powersensor OK")
            status = True
        else:
            status_ps = False
            messages = messages + "Issue : impossible to get powersensor status \n"

        if messages != "":
            logging.error(messages)
            status = self.alerter.sendAlert(messages)
        else:
            status = status_ps and status_inverter

        return status

    def control_rules(self):
        self.refresh_data()
        # sort rule by priority
        rules = sorted(self.power_rules.rules, key=lambda x: x['rule_priority'])
        estimated_remaining_power = self.dev_mgmt.ps.power
        logging.info("Remaining power : " + str(estimated_remaining_power))
        disable_flag = False
        for rule in rules:
            dev_name = rule['action_device_name']
            dev_type = rule['action_device_type']
            status = self.action_devices_mgmt.get_device_status(dev_type, dev_name)
            bool_status = None
            if status != None:
                bool_status = status["status"]
            if estimated_remaining_power != None:
                if estimated_remaining_power >= 0:
                    # if there is power
                    if estimated_remaining_power >= rule['rule_remaining_power_value']:
                        # if there is enough power for this device

                        # case device status OFF and need to be power ON:
                        if bool_status == False and rule['action_threshold_crossed'] == "enable":
                            if self.action_devices_mgmt.enable_device(dev_type, dev_name):
                                logging.info(dev_name + " successfully power ON !")
                                estimated_remaining_power = estimated_remaining_power - rule['rule_remaining_power_value']
                            else:
                                logging.error("Error when try to power ON : " + dev_name)

                        # case device status ON and need to be power ON:
                        if bool_status == True and rule['action_threshold_crossed'] == "enable":
                            logging.info("device " + dev_name + " already ON")

                        # case device status ON and need to be power OFF (why disable when generate power? idk):
                        if bool_status == True and rule['action_threshold_crossed'] == "disable":
                            if self.action_devices_mgmt.disable_device(dev_type, dev_name):
                                logging.info(dev_name + " successfully power OFF")
                                estimated_remaining_power = estimated_remaining_power - rule['rule_remaining_power_value']
                            else:
                                logging.error("Error when try to power OFF: " + dev_name)

                        # case device status OFF and need to be power OFF (why disable when generate power ? idk):
                        if bool_status == False and rule['action_threshold_crossed'] == "disable":
                            logging.info("device " + dev_name + " already OFF")
                    else:
                        # if there is NOT enough power for this device :

                        if bool_status == False:
                            logging.info("device " + dev_name + " already OFF")

                        # case device already ON, keep it as-is
                        if bool_status == True:
                            logging.info("device " + dev_name + " already ON")
                        # case device powered OFF, keep it as-is
                        else:
                            logging.info("not enough power to start : "+ dev_name)

                else:
                    #case we cannot get value from Huawei cloud
                    logging.info("Not enough power produced : Disable")
                    disable_flag = True
            else:
                # case powered from main electrical grid or data not reachable as we are not sure we power off device:
                logging.info("Issue to get data from Huawei : Disable")
                disable_flag = True
            if disable_flag:
                if self.action_devices_mgmt.disable_device(dev_type,dev_name):
                    logging.info(dev_name + " successfully power OFF")
                else:
                    logging.error("Error when trying to power off : " + dev_name)

