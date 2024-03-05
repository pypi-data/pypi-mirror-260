from .base import (InfuzuError, NotFoundError)


class UserSubscriptionError(InfuzuError):
    pass


class UserSubscriptionNotFoundError(UserSubscriptionError, NotFoundError):
    pass
