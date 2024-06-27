
class PowerUsageRules():

    rules = [{'rule_id': 1,
              'rule_name': "Pool Heating Threshold",
              'rule_type': "threshold",
              'rule_remaining_power_value': 1000,
              'rule_priority': 1,
              'action_threshold_crossed': 'enable',
              'action_device_name': 'PAC piscine',
              'action_device_type': 'philips_hue'
              }
              ]
