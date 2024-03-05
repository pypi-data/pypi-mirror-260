class CheckoutSDKError(Exception):
    def __init__(self, message: str):
        super().__init__(message)



class APIError(CheckoutSDKError):
    def __init__(self, status_code: int, error_code: str, message: str):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        super().__init__(f"API Error: Status Code {status_code}, Error Code: {error_code}, Message: {message}")

class InvalidParameterError(CheckoutSDKError):

    def __init__(self, parameter_name: str, message: str = None):
        self.parameter_name = parameter_name
        super().__init__(f"Invalid parameter '{parameter_name}'." + (f" {message}" if message else ""))