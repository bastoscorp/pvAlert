# pvAlert : monitor Huawei SUN2000 interver

pvAlert is a script that monitor system monitor Huawei SUN2000 inverter and powersensor and alerts (throughout notify.sh) you whenever there is a malfunction in your solar system field.

Thanks to ntfy.sh you can be alreted directly onto your smartphone.

It can also power on/off devices connected to a philips hue smart plug according to your electricity production.

---
## Requirements: 

pvAlert can run on a several systems, it needs :

| Required | Component                         | Version | Description                                                           | 
| ------------ |-----------------------------------| --------  |-----------------------------------------------------------------------|
| Required | Python                            | 3.9 | pvAlert execution runtime                                             |
| Required | ntfy.sh topic                     | N/A | A ntfy.sh topic to be alerted, available freely here https://ntfy.sh/ |
| Required | OpenAPI account (Huawei Cloud)    | N/A | Necessary to reach Huawei cloud to get status                         |
| Optionnal | Philips Hue bridge and smart plug | latest | Only if you want to control electrical appliances according to your energy production |

Note : I prefer to precise that an **internet connection is required.**

---

## Installation :

Very simple, if you have git installed on your target execute this :

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/bastoscorp/pvAlert/main/install_pvAlert_with_git.sh)"`

If you don't have git installed on your target do this:

1. Download latest tag : https://github.com/bastoscorp/pvAlert/tags
2. Uncompress it into pvAlert folder
3. Run install_pvAlert_manual.sh


## Configuration :

All configuration is done within `config.ini` file.
You need to fulfill at bare minimum the following fields:

| Section | Field | Description                                    | Value                                                                                       |
|---------|-------|------------------------------------------------|---------------------------------------------------------------------------------------------|
| General | user  | Huawei OpenAPI user                            | Username you provide, <br/>Check "Getting an Huawei OpenAPI account" in helper section      |
| General | password | Huawei OpenAPI user password encoded in base64 | The password you given for your Huawei user <br/> Check "Base64 encoding" in helper section |
| alert | topic | topic name                                   | Topic you have created on ntfy.sh                                                           |
| alert | title | notification title | A given title to your notification                                                          |

If you want just the alerting part of the application please comment last line of main.py file by adding a '#' at begining of the line and go to the next part of the document:

```commandline
#conso_manager.control_rules()
```

If you want to use power on/off with philips hue smart plug you need:

1. To provide a couple more values:

| Section | Field | Description            | Value                                                                                       |
|---------|-------|------------------------|---------------------------------------------------------------------------------------------|
| action_philips_hue | hue_username  | Philips Hue username   | Check "Getting Philips Hue key" in helper section      |
| action_philips_hue | hue_client_key | Philips Hue client key | Check "Getting Philips Hue key" in helper section |

2. Make sure conso_manager.control_rules() is called, by deleting '#' at the begining of the line:

```commandline
conso_manager.control_rules()
```

3. Provide information about your Philips Hue smart plug:

In `business/powerUsageRules.py` fill the "rules" array:


```commandline
 rules = [
              {'rule_id': 1,
              'rule_name': "You rule name",
              'rule_remaining_power_value': 1200, 
              'rule_priority': 1, 
              'action_threshold_crossed': 'enable', 
              'action_device_name': 'PAC piscine', 
              'action_device_type': 'philips_hue' 
              },
              {'rule_id': 2,
              'rule_name': "Your rule name",
              'rule_remaining_power_value': 1000,
              'rule_priority': 2,
              'action_threshold_crossed': 'enable',
              'action_device_name': '',
              'action_device_type': 'philips_hue'
              }
              ]
```

Rules field documentation :

| Field name                 | Value type                                             | Required/Opionnal | Description                                                                                                                                                |
|----------------------------|--------------------------------------------------------|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rule_id                    | Integer                                                | Required          | Rule identifier                                                                                                                                            |
| rule_name                  | String                                                 | Optionnal         | The rule name                                                                                                                                              |
| rule_remaining_power_value | Integer                                                | Required | Number of Watt (and not kWh) you need to produce to enable/disable your device                                                                             |
| rule_prority               | Integer                                                | Required | Priority number of your device<br/> small values has higher priority:  <br/> - 1 has high priority over 2 <br/> - 2 has high priority over 3<br/> - etc... |                                                         
| action_threshold_crossed   | String<br/>Allowed values : "enable" or "disable"      | Required | Device action when you exceed the remaining power value. <br/> Action can be enable or disable                                                             |
| action_device_name         | String                                                 | Required | Device controler name or identifier                                                                                                                        |
| action_device_type         | String<br/>Allowed value at the moment : "philips_hue" | Required | Device controler type<br/>At the moment it only works with Philips Hue smart plug                                                                          |

## Scheduling :

If you are on *nix (macos included) system just provide the execute right to `register_cron.sh` file by typing : `chmod +x register_cron.sh`

pvAlert will now run each 5 minutes from 8:00AM to 10:00PM (no need to run at night)

If you want to delete scheduling you can `useunregister_cron.sh` file.

On Windows system you can use task scheduler.

---
## Helper section: 
### 1. Getting an Huawei OpenAPI account:

1. Connect to Fusion Solar website: https://eu5.fusionsolar.huawei.com ( I don't know if there is other subdomain for other location than Europe...)
2. Login with "company administrator user"
3. You need to go into **System > Company Management > Northbound Management** 
4. Then click Add
5. Provide username and password 
6. Search and select your plan 
7. Enable "provide Real-time monitoring report and alarm ..."

All those steps are described here : https://support.huawei.com/enterprise/fr/doc/EDOC1100366278/fba05f66



### 2. Getting Philips Hue key:

1. First get your bridge ip address navigate to : https://discovery.meethue.com/
2. Go to your Philips hue bridge and press the button
3. With curl utility replace {bridge_ip_address} with "internalipaddress" value from first point then execute

`
curl -k -d '{ "devicetype": "app_name#instance_name", "generateclientkey": true }' https://{bridge_ip_address}/api
`

You should get an answer like :
```
[
    {
        "success": {
            "username": "xxxxxxxxxxxxxXXXXXXxxxxxXXXXXXxxxxXXXXXx",
            "clientkey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        }
    }
]
```

if you get the following answer this means that you need to press your bridge's button:
```
[{"error":{"type":101,"address":"","description":"link button not pressed"}}]
```

Note: if you don't have curl you can use postman or another tool. It just needs to do a http POST with parameters

Philips developer documentation link here : https://developers.meethue.com/develop/hue-api-v2/getting-started/

### 3. Base64 encoding:

If you are on *nix systems (included macos) you can use terminal with the following command:
`echo "youhou" | base64`

Otherwhise you can visit https://www.base64decode.org/

---






# Todo list :

- [X] *nix crontab script
- [X] *nix run script
- [ ] batch / powershell scripts
- [ ] Docker Image

