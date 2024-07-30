from fastapi import HTTPException, status


class BException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class PasswordNotValidException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Password is not valid"


class UserAlreadyExistsException(BException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class UserNotFoundException(BException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"
