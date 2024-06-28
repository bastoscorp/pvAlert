
class InverterRules:

    ok_status = 512
    ko_status = 768


    status_list = {
        "0":{"message": "Standby: initializing", "type": "warning"},
        "1":{"message":"Standby: insulation resistance detecting", "type": "warning"},
        "2":{"message":"Standby: irradiation detecting", "type": "warning"},
        "3":{"message":"Standby: grid detecting", "type": "warning"},
        "256":{"message":"Start", "type": "ok"},
        "512":{"message":"Grid-connected", "type": "ok"},
        "513":{"message":"Grid-connected: power limited", "type": "ok"},
        "514":{"message":"Grid-connected: self-derating", "type": "ok"},
        "515":{"message":"Off-grid operation","type": "warning"},
        "768":{"message":"Shutdown: on fault", "type": "error"},
        "769":{"message":"Shutdown: on command", "type": "error"},
        "770":{"message":"Shutdown: OVGR", "type": "error"},
        "771":{"message":"Shutdown: communication interrupted", "type": "error"},
        "772":{"message":"Shutdown: power limited", "type": "error"},
        "773":{"message":"Shutdown: manual startup required", "type": "error"},
        "774":{"message":"Shutdown: DC switch disconnected", "type": "error"},
        "775":{"message":"Shutdown: rapid shutdown","type": "error"},
        "776":{"message":"Shutdown: input underpower","type": "error"},
        "777":{"message":"Shutdown: NS protection","type": "error"},
        "778":{"message":"Shutdown: commanded rapid shutdown","type": "error"},
        "1025":{"message":"Grid scheduling: cosφ-P curve", "type": "warning"},
        "1026":{"message":"Grid scheduling: Q-U curve","type": "warning"},
        "1027":{"message":"Power grid scheduling: PF-U characteristic curve","type": "warning"},
        "1028":{"message":"Grid scheduling: dry contact","type": "warning"},
        "1029":{"message":"Power grid scheduling: Q-P characteristic curve","type": "warning"},
        "1280":{"message":"Ready for terminal test","type": "warning"},
        "1281":{"message":"Terminal testing...","type": "warning"},
        "1536":{"message":"Inspection in progress","type": "warning"},
        "1792":{"message":"AFCI self-check","type": "warning"},
        "2048":{"message":"I-V scanning","type": "warning"},
        "2304":{"message":"DC input detection","type": "warning"},
        "2560":{"message":"Off-grid charging","type": "warning"},
        "40960":{"message":"Standby: no irradiation","type": "warning"},
        "40961":{"message":"Standby: no DC input","type": "warning"},
        "45056":{"message":"Communication interrupted (written by SmartLogger)","type": "error"},
        "49152":{"message":"Loading... (written by SmartLogger)","type": "warning"},
    }

