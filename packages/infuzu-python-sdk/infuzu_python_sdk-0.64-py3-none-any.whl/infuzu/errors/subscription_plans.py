from .base import (InfuzuError, NotFoundError, EligibilityError)


class SubscriptionPlanError(InfuzuError):
    pass


class SubscriptionPlanNotFoundError(SubscriptionPlanError, NotFoundError):
    pass


class SubscriptionPlanEligibilityError(SubscriptionPlanError, EligibilityError):
    pass
