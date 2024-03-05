from .base import EligibilityError
from .subscriptions import SubscriptionError
from .users import UserError


class UserAndSubscriptionError(UserError, SubscriptionError):
    pass


class UserAndSubscriptionNotEligibleError(UserAndSubscriptionError, EligibilityError):
    pass
