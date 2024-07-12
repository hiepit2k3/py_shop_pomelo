class CustomAPIException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class BadRequestException(CustomAPIException):
    def __init__(self, message="Bad Request"):
        super().__init__(message, 400)

class NotFoundException(CustomAPIException):
    def __init__(self, message="Not Found"):
        super().__init__(message, 404)

class ConflictException(CustomAPIException):
    def __init__(self, message="Conflict"):
        super().__init__(message, 409)

class InternalServerException(CustomAPIException):
    def __init__(self, message="Internal Server Error"):
        super().__init__(message, 500)
