from dataclasses import dataclass
from requests import Response
from .. import constants
from ..errors.base import InfuzuError
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem


OBJECT_ACCESS_PROFILE_CACHE: CacheSystem = CacheSystem(default_expiry_time=60)


@dataclass
class ObjectAccessProfile:
    user_id: str | None
    object_type: str
    owned: list[str]
    explicit_definition_editor: list[str]
    explicit_definition_viewer: list[str]
    explicit_product_user: list[str]
    implicit_definition_editor: list[str]
    implicit_definition_viewer: list[str]
    implicit_product_user: list[str]

    def get_access_list(self, **kwargs) -> list[str]:
        final_list: list[str] = []
        if kwargs.get('owned', False):
            final_list.extend(self.owned)
        if kwargs.get('explicit_definition_editor', False):
            final_list.extend(self.explicit_definition_editor)
        if kwargs.get('explicit_definition_viewer', False):
            final_list.extend(self.explicit_definition_viewer)
        if kwargs.get('explicit_product_user', False):
            final_list.extend(self.explicit_product_user)
        if kwargs.get('implicit_definition_editor', False):
            final_list.extend(self.implicit_definition_editor)
        if kwargs.get('implicit_definition_viewer', False):
            final_list.extend(self.implicit_definition_viewer)
        if kwargs.get('implicit_product_user', False):
            final_list.extend(self.implicit_product_user)
        final_unique_list: list[str] = list(set(final_list))
        return final_unique_list

    @classmethod
    def retrieve(cls, user_id: str | None, object_type: str) -> 'ObjectAccessProfile':
        if not user_id:
            user_id: str = 'null'

        def get_object_access_profile() -> 'ObjectAccessProfile':
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.ACCESS_BASE_URL}"
                    f"{constants.ACCESS_RETRIEVE_OBJECT_ACCESS_PROFILE_ENDPOINT}"
                .replace('<str:user_id>', user_id).replace('<str:object_type>', object_type)
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            raise InfuzuError(f"Error retrieving object access profile: {api_response.text}")
        return OBJECT_ACCESS_PROFILE_CACHE.get(
            cache_key_name=f'{user_id}__{object_type}', specialized_fetch_function=get_object_access_profile
        )
