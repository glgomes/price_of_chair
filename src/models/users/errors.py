__author__ = 'glgs'


class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistsError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass


class UserAlreadyExistsError(UserError):
    pass


class MalformedEmail(UserError):
    pass