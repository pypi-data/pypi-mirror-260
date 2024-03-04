class CustomException(Exception):
    pass


class AccessDenied(CustomException):
    pass


class NotFound(CustomException):
    pass
