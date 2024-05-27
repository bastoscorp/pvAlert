class HuaweiApiException(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...

        errStr = "Error : " + errors["data"] + " failCode : " + errors["failCode"]
        self.errors = errStr