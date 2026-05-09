class AppError(Exception):
    pass


class NotAuthenticatedError(AppError):
    pass


class InvalidTokenError(AppError):
    pass


class InvalidCredentialsError(AppError):
    pass


class InvalidSessionError(AppError):
    pass


class EmailAlreadyRegisteredError(AppError):
    pass


class UsernameAlreadyTakenError(AppError):
    pass


class ListNotFoundError(AppError):
    pass


class TaskNotFoundError(AppError):
    pass
