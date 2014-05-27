class SapiException(Exception):
    pass

class ApiException(SapiException):
    pass

class ApiError(ApiException):
    pass

class CsrNotAuthedError(ApiError):
    pass

class CaUpdateCancelledException(SapiException):
    pass
