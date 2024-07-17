from config.config import Config
from business.actionDevicePhilipsHue import ActionDevicePhilipsHue
import logging
from random import randrange


class ActionDeviceManager:
    config: Config = None
    testing_status = {}

    def __init__(self, conf: Config):
        self.config = conf

    def get_device_status(self, dev_type: str, dev_name: str):
        status = None
        if dev_type == "philips_hue":
            dev_manager: ActionDevicePhilipsHue = ActionDevicePhilipsHue(self.config)
            status = dev_manager.get_device_status(dev_name)
            return status
        if dev_type == "testing":
            if self.testing_status.get(dev_name) is None:
                if randrange(10) % 2 == 0:
                    status = {'status': True,
                              'message': "powered on"
                              }
                else:
                    status = {'status': False,
                              'message': "powered off"
                              }
                self.testing_status[dev_name] = status
            return self.testing_status.get(dev_name)
        else:
            logging.warning(dev_type + " device type not implemented")
        return status

    def enable_device(self, dev_type: str, dev_name: str):
        status = None
        if dev_type == "philips_hue":
            dev_manager: ActionDevicePhilipsHue = ActionDevicePhilipsHue(self.config)
            status = dev_manager.enable_plug(dev_name)
            return status
        if dev_type == "testing":
            status = {'status': True,
                      'message': "powered on"
                      }
            self.testing_status[dev_name] = status
            return True
        else:
            logging.warning(dev_type + " device type not implemented")
        return status

    def disable_device(self, dev_type: str, dev_name: str):
        status = None
        if dev_type == "philips_hue":
            dev_manager: ActionDevicePhilipsHue = ActionDevicePhilipsHue(self.config)
            status = dev_manager.disable_plug(dev_name)
            return status
        if dev_type == "testing":
            status = {'status': False,
                      'message': "powered off"
                      }
            self.testing_status[dev_name] = status
            return True
        else:
            logging.warning(dev_type + " device type not implemented")
        return status

