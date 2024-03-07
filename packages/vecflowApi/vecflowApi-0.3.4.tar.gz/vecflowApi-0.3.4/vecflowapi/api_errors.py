class APIError(Exception):
    def __init__(self, status_code, message=None):
        super().__init__()
        self.status_code = status_code
        self.message = message


class NotFoundAPIError(APIError):
    def __init__(self, message=None):
        if message is None:
            super().__init__(404, "Resource Not Found")
        else:
            super().__init__(404, message)


class InternalServerAPIError(APIError):
    def __init__(self, message=None):
        if message is None:
            super().__init__(500, "Internal Server error")
        else:
            super().__init__(500, message)


class BadRequestAPIError(APIError):
    def __init__(self, status_code=400, message=None):
        """
        Initialize a BadRequestAPIError.

        :param message: The error message describing the bad request issue. Defaults to None.
        :type message: str
        """
        if message is None:
            super().__init__(status_code, "Bad Request")
        else:
            super().__init__(status_code, message)


class UnauthorizedAPIError(APIError):
    def __init__(self, message=None):
        """
        Initialize an UnauthorizedAPIError.

        :param message: The error message describing the unauthorized access issue. Defaults to None.
        :type message: str
        """
        if message is None:
            super().__init__(401, "Unauthorized")
        else:
            super().__init__(401, message)


class ForbiddenAPIError(APIError):
    def __init__(self, message=None):
        """
        Initialize a ForbiddenAPIError.

        :param message: The error message describing the forbidden access issue. Defaults to None.
        :type message: str
        """
        if message is None:
            super().__init__(403, "Forbidden")
        else:
            super().__init__(403, message)
