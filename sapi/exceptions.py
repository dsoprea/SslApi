class SapiException(Exception):
    pass

class ApiException(SapiException):
    pass

class ApiError(ApiException):
    pass

class CsrSignError(ApiError):
    pass

class CaUpdateCancelledException(SapiException):
    pass
