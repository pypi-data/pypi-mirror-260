import datetime
from dataclasses import dataclass
from decimal import Decimal
from requests import Response
from .user_subscription import UserSubscription
from .. import constants
from ..errors.base import InfuzuError
from ..errors.subscription_plans import (SubscriptionPlanEligibilityError, SubscriptionPlanNotFoundError)
from ..errors.subscriptions import SubscriptionEligibilityError
from ..errors.users import UserNotFoundError
from ..http_requests import signed_requests


@dataclass
class SubscriptionPlan:
    id: str
    subscription: str
    created_at: str
    last_updated_at: str
    name: str
    length: int
    price_usd: str
    display_publicly: bool
    allow_more_subscriptions: bool

    @property
    def created_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.created_at)

    @property
    def last_updated_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.last_updated_at)

    @property
    def length_timedelta(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self.length)

    @property
    def price_usd_decimal(self) -> Decimal:
        return Decimal(self.price_usd)

    def subscribe(self, user_id: str) -> UserSubscription:
        if not self.allow_more_subscriptions:
            raise SubscriptionPlanEligibilityError("Subscription Plan does allow more subscriptions")
        url: str = (
            f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_SUBSCRIBE_TO_PLAN}"
            .replace('<str:subscription_plan_id>', self.id).replace('<str:user_id>', user_id)
        )

        def create_subscription() -> UserSubscription:
            api_response: Response = signed_requests.request(method="POST", url=url)
            if api_response.status_code == 201:
                return UserSubscription(**api_response.json())
            elif api_response.status_code == 403:
                if api_response.json().get("error") == "subscription_plan_not_allow_more_subscriptions":
                    raise SubscriptionPlanEligibilityError(api_response.json()["message"])
                elif api_response.json().get("error") == "subscription_not_allow_more_subscriptions":
                    raise SubscriptionEligibilityError(api_response.json()["message"])
            elif api_response.status_code == 404:
                if api_response.json().get("error") == "user_does_not_exist":
                    raise UserNotFoundError(api_response.json()["message"])
                elif api_response.json().get("error") == "subscription_plan_does_not_exist":
                    raise SubscriptionPlanNotFoundError(api_response.json()["message"])
            raise InfuzuError(f"Error activating free trial: {api_response.text}")

        return create_subscription()
