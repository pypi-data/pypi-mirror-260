class OrcaException(Exception):
    """
    Base exception type of Orca
    :param message: The error message
    :param content: The http content of the request if available
    """

    def __init__(self, message, content=None):
        self.content = content
        super(OrcaException, self).__init__(message)


class OrcaNotFoundException(OrcaException):
    pass


class OrcaUnauthenticatedException(OrcaException):
    pass


class OrcaUnauthorizedException(OrcaException):
    pass


class OrcaBadRequestException(OrcaException):
    pass
