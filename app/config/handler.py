from fastapi import HTTPException, status
from pymongo.errors import PyMongoError, DuplicateKeyError,ServerSelectionTimeoutError

class UsernameAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is already taken, please choose another."
        )

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!."
        )

class MongoDBExceptionHandler:
    @staticmethod
    def handle_mongo_error(error: PyMongoError):
        if isinstance(error, DuplicateKeyError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate entry in MongoDB."
            )
        elif isinstance(error, ServerSelectionTimeoutError):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not connect to MongoDB, please try again later."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal server error occurred with MongoDB."
            )


class PasswordConfirmException(HTTPException):
    def __init__(self):
        super().__init__(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Password and confirm password doesn't match."
    )

class EmailValidationException(HTTPException):
    def __init__(self):
        super().__init__(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email is not valid."
    )

class BlogNotFound(HTTPException):
    def __init__(self):
        super().__init__(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Blog not found."
    )

class CommentNotFound(HTTPException):
    def __init__(self):
        super().__init__(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Comment not found."
    )

class UnauthorizedAction(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized for this action."
        )

class WrongPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password."
        )

class UnExpectedError(HTTPException):
    def __init__(self):
        super().__init__(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unexpected error occurred."
    )

class PasswordValidationException(HTTPException):
    def __init__(self):
        super().__init__(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Password is not valid."
    )