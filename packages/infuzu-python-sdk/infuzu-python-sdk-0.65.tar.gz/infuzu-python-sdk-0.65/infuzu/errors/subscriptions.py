from .base import (InfuzuError, NotFoundError, EligibilityError)


class SubscriptionError(InfuzuError):
    pass


class SubscriptionNotFoundError(SubscriptionError, NotFoundError):
    pass


class SubscriptionEligibilityError(SubscriptionError, EligibilityError):
    pass
