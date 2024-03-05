from .base import (InfuzuError, NotFoundError)


class UserError(InfuzuError):
    pass


class UserNotFoundError(UserError, NotFoundError):
    pass
