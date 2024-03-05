from dataclasses import dataclass
from requests import Response
from .. import constants
from ..errors.base import InfuzuError
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem


USER_ACCESS_PROFILE_CACHE: CacheSystem = CacheSystem(default_expiry_time=60)


@dataclass
class UserAccessProfile:
    user_id: str | None
    billing_in_good_standing: bool
    active_subscriptions: list[str]

    @classmethod
    def retrieve(cls, user_id: str) -> 'UserAccessProfile':
        if not user_id:
            user_id: str = 'null'

        def get_user_access_profile() -> 'UserAccessProfile':
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.ACCESS_BASE_URL}"
                    f"{constants.ACCESS_RETRIEVE_USER_ACCESS_PROFILE_ENDPOINT}".replace('<str:user_id>', user_id)
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            raise InfuzuError(f"Error retrieving user access profile: {api_response.text}")
        return USER_ACCESS_PROFILE_CACHE.get(
            cache_key_name=f'{user_id}', specialized_fetch_function=get_user_access_profile
        )
