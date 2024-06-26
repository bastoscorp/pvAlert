
class InverterRules:

    ok_status = 512
    ko_status = 768


    status_list = {
        "0":"Standby: initializing",
        "1":"Standby: insulation resistance detecting",
        "2":"Standby: irradiation detecting",
        "3":"Standby: grid detecting",
        "256":"Start",
        "512":"Grid-connected",
        "513":"Grid-connected: power limited",
        "514":"Grid-connected: self-derating",
        "515":"Off-grid operation",
        "768":"Shutdown: on fault",
        "769":"Shutdown: on command",
        "770":"Shutdown: OVGR",
        "771":"Shutdown: communication interrupted",
        "772":"Shutdown: power limited",
        "773":"Shutdown: manual startup required",
        "774":"Shutdown: DC switch disconnected",
        "775":"Shutdown: rapid shutdown",
        "776":"Shutdown: input underpower",
        "777":"Shutdown: NS protection",
        "778":"Shutdown: commanded rapid shutdown",
        "1025":"Grid scheduling: cosφ-P curve",
        "1026":"Grid scheduling: Q-U curve",
        "1027":"Power grid scheduling: PF-U characteristic curve",
        "1028":"Grid scheduling: dry contact",
        "1029":"Power grid scheduling: Q-P characteristic curve",
        "1280":"Ready for terminal test",
        "1281":"Terminal testing...",
        "1536":"Inspection in progress",
        "1792":"AFCI self-check",
        "2048":"I-V scanning",
        "2304":"DC input detection",
        "2560":"Off-grid charging",
        "40960":"Standby: no irradiation",
        "40961":"Standby: no DC input",
        "45056":"Communication interrupted (written by SmartLogger)",
        "49152":"Loading... (written by SmartLogger)",
    }

