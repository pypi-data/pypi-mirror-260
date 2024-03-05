import json
from dataclasses import dataclass
from datetime import datetime
from requests import Response
from .. import constants
from ..errors.base import (InfuzuError, MissingRequiredFieldError, InputFormatError, InvalidFieldError, InputTypeError)
from ..errors.subscription_plans import (SubscriptionPlanEligibilityError, SubscriptionPlanNotFoundError)
from ..errors.subscriptions import (SubscriptionEligibilityError, SubscriptionNotFoundError)
from ..errors.user_subscriptions import UserSubscriptionNotFoundError
from ..errors.users import UserNotFoundError
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem


USER_SUBSCRIPTION_CACHE: CacheSystem = CacheSystem(default_expiry_time=60)


@dataclass
class UserSubscription:
    id: str
    user: str
    subscription: str
    subscription_plan: str | None
    created_at: str
    start_at: str
    expire_at: str
    is_active: bool

    @property
    def created_at_datetime(self) -> datetime:
        return datetime.fromisoformat(self.created_at)

    @property
    def start_at_datetime(self) -> datetime:
        return datetime.fromisoformat(self.start_at)

    @property
    def expire_at_datetime(self) -> datetime:
        return datetime.fromisoformat(self.expire_at)

    @classmethod
    def create(
            cls,
            user_id: str,
            subscription_id: str,
            start_at: datetime,
            expire_at: datetime,
            subscription_plan_id: str | None = None
    ) -> 'UserSubscription':
        data_params: dict[str, any] = {
            "user_id": user_id,
            "subscription_id": subscription_id,
            "start_at": start_at.isoformat(),
            "expire_at": expire_at.isoformat(),
        }
        if subscription_plan_id:
            data_params["subscription_plan_id"] = subscription_plan_id

        def create_user_subscription() -> 'UserSubscription':
            api_response: Response = signed_requests.request(
                method="POST",
                url=f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_CREATE_USER_SUBSCRIPTION}",
                json=data_params
            )
            if api_response.status_code == 201:
                return cls(**api_response.json())
            elif api_response.status_code == 400:
                if api_response.json().get("error") == "missing_field":
                    raise MissingRequiredFieldError(api_response.json()["message"])
                elif api_response.json().get("error") == "format_error":
                    raise InputFormatError(api_response.json()["message"])
            elif api_response.status_code == 403:
                if api_response.json().get("error") == "subscription_not_allow_more_subscriptions":
                    raise SubscriptionEligibilityError(api_response.json()["message"])
                elif api_response.json().get("error") == "subscription_plan_not_allow_more_subscriptions":
                    raise SubscriptionPlanEligibilityError(api_response.json()["message"])
            elif api_response.status_code == 404:
                if api_response.json().get("error") == "user_does_not_exist":
                    raise UserNotFoundError(api_response.json()["message"])
                elif api_response.json().get("error") == "subscription_does_not_exist":
                    raise SubscriptionNotFoundError(api_response.json()["message"])
                elif api_response.json().get("error") == "subscription_plan_does_not_exist":
                    raise SubscriptionPlanNotFoundError(api_response.json()["message"])
            raise InfuzuError(f"Error creating user subscription: {api_response.text}")
        return create_user_subscription()

    @classmethod
    def retrieve(cls, id: str) -> 'UserSubscription':
        def get_user_subscription() -> 'UserSubscription':
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_RETRIEVE_USER_SUBSCRIPTION}"
                .replace('<str:user_subscription_id>', id)
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            elif api_response.status_code == 404:
                if api_response.json().get("error") == "user_subscription_does_not_exist":
                    raise UserSubscriptionNotFoundError(api_response.json()["message"])
            raise InfuzuError(f"Error retrieving user subscription: {api_response.text}")

        return USER_SUBSCRIPTION_CACHE.get(
            cache_key_name=f'user_subscription-{id}', specialized_fetch_function=get_user_subscription
        )

    @classmethod
    def retrieve_ids(cls, **filters) -> list[str]:
        ALLOWED_FILTERS: dict[str, type] = {"user_id": str, "subscription_id": str, "is_active": bool}
        new_params: dict[str, str] = {}
        for param_key, param_value in filters.items():
            if param_key not in ALLOWED_FILTERS:
                raise InvalidFieldError(
                    f"Invalid filter parameter: {param_key}. Must be one of {list(ALLOWED_FILTERS.keys())}"
                )
            if not isinstance(param_value, ALLOWED_FILTERS[param_key]):
                raise InputTypeError(
                    f"Invalid type for filter parameter: {param_key}. Must be {ALLOWED_FILTERS[param_key]}"
                )
            new_params[param_key] = str(param_value)

        def get_user_subscriptions() -> list[str]:
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_RETRIEVE_USER_SUBSCRIPTIONS}",
                params=new_params
            )
            if api_response.status_code == 200:
                return api_response.json()
            raise InfuzuError(f"Error retrieving user subscriptions: {api_response.text}")

        return USER_SUBSCRIPTION_CACHE.get(
            cache_key_name=f'user_subscriptions-{json.dumps(new_params)}',
            specialized_fetch_function=get_user_subscriptions
        )
