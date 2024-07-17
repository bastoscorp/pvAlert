
class PowersensorDevice:

    device_type_code: int = 47
    device_id = ""
    device_name = ""

    status: int = None
    # 1 mean --> OK
    # other mean --KO

    power: float = None
    # 100
    # -3159.0
