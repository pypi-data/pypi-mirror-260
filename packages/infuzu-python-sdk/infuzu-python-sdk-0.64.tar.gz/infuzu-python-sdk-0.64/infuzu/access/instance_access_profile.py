import datetime
from dataclasses import dataclass
from enum import Enum
from requests import Response
from .user_access_profile import UserAccessProfile
from .. import constants
from ..errors.base import InfuzuError
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem
from ..utils.enums.checks import validate_enum_value


INSTANCE_ACCESS_PROFILE_CACHE: CacheSystem = CacheSystem(default_expiry_time=60)


class WhoHasAccessEnum(Enum):
    RESTRICTED: str = "R"
    ANYONE_SIGNED_IN: str = "S"
    ANYONE_WITH_LINK: str = "A"


class LinkAccessEnum(Enum):
    DEFINITION_EDITOR: str = "DE"
    DEFINITION_VIEWER: str = "DV"
    PRODUCT_USER: str = "PU"


class PaymentOptionEnum(Enum):
    OWNER: str = "O"
    OWNER_AND_SUBSCRIPTION: str = "OS"
    USER: str = "U"
    OWNER_AND_SUBSCRIPTION_WITH_USER_AS_BACKUP: str = "OB"


@dataclass
class InstanceAccessProfile:
    id: str
    object_type: str
    who_has_access: str
    link_access: str
    owner_id: str
    definition_editors: list[str]
    definition_viewers: list[str]
    product_users: list[str]
    payment_option: str
    subscribed_users: list[str]
    subscription_list: list[str]
    last_updated: str

    @property
    def who_has_access_enum(self) -> WhoHasAccessEnum:
        return WhoHasAccessEnum(self.who_has_access)

    @property
    def link_access_enum(self) -> LinkAccessEnum:
        return LinkAccessEnum(self.link_access)

    @property
    def payment_option_enum(self) -> PaymentOptionEnum:
        return PaymentOptionEnum(self.payment_option)

    @property
    def last_updated_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.last_updated)

    def is_owner(self, user_id: str | None) -> bool:
        return self.owner_id == user_id

    def is_explicit_definition_editor(self, user_id: str | None) -> bool:
        return user_id in self.definition_editors

    def is_explicit_definition_viewer(self, user_id: str | None) -> bool:
        return user_id in self.definition_viewers

    def is_explicit_product_user(self, user_id: str | None) -> bool:
        return user_id in self.product_users

    def has_link_access(self, user_id: str | None) -> bool:
        return self.who_has_access_enum == WhoHasAccessEnum.ANYONE_WITH_LINK or (
            self.who_has_access_enum == WhoHasAccessEnum.ANYONE_SIGNED_IN and user_id
        )

    def is_implicit_definition_editor(self, user_id: str | None) -> bool:
        return self.has_link_access(user_id) and self.link_access_enum == LinkAccessEnum.DEFINITION_EDITOR

    def is_implicit_definition_viewer(self, user_id: str | None) -> bool:
        return self.has_link_access(user_id) and self.link_access_enum == LinkAccessEnum.DEFINITION_VIEWER

    def is_implicit_product_user(self, user_id: str | None) -> bool:
        return self.has_link_access(user_id) and self.link_access_enum == LinkAccessEnum.PRODUCT_USER

    def is_definition_editor(self, user_id: str | None) -> bool:
        return (
            self.is_explicit_definition_editor(user_id) or
            self.is_implicit_definition_editor(user_id) or
            self.is_owner(user_id)
        )

    def is_definition_viewer(self, user_id: str | None) -> bool:
        return (
            self.is_explicit_definition_viewer(user_id) or
            self.is_implicit_definition_viewer(user_id) or
            self.is_definition_editor(user_id)
        )

    def is_product_user(self, user_id: str | None) -> bool:
        return (
                self.is_explicit_product_user(user_id) or
                self.is_implicit_product_user(user_id) or
                self.is_definition_viewer(user_id)
        )

    def has_subscription(self, user_id: str | None) -> bool:
        return user_id in self.subscribed_users

    @property
    def requires_subscription(self) -> bool:
        return self.payment_option_enum == PaymentOptionEnum.OWNER_AND_SUBSCRIPTION

    def has_use_access(self, user_id: str | None) -> bool:
        if self.payment_option_enum == PaymentOptionEnum.OWNER:
            return self.is_product_user(user_id)
        elif self.payment_option_enum == PaymentOptionEnum.OWNER_AND_SUBSCRIPTION:
            return self.is_product_user(user_id) and self.has_subscription(user_id)
        elif self.payment_option_enum == PaymentOptionEnum.USER:
            return self.is_product_user(user_id) and UserAccessProfile.retrieve(user_id).billing_in_good_standing
        elif self.payment_option_enum == PaymentOptionEnum.OWNER_AND_SUBSCRIPTION_WITH_USER_AS_BACKUP:
            return self.is_product_user(user_id) and (
                    self.has_subscription(user_id) or UserAccessProfile.retrieve(user_id).billing_in_good_standing
            )
        else:
            raise NotImplementedError(f"Payment option {self.payment_option_enum} not implemented.")

    def user_id_to_charge(self, user_id: str | None) -> str | None:
        if self.payment_option_enum == PaymentOptionEnum.OWNER:
            return self.owner_id
        elif self.payment_option_enum == PaymentOptionEnum.OWNER_AND_SUBSCRIPTION:
            return self.owner_id
        elif self.payment_option_enum == PaymentOptionEnum.USER:
            return user_id
        elif self.payment_option_enum == PaymentOptionEnum.OWNER_AND_SUBSCRIPTION_WITH_USER_AS_BACKUP:
            return self.owner_id if self.has_subscription(user_id) else user_id
        else:
            raise NotImplementedError(f"Payment option {self.payment_option_enum} not implemented.")

    @classmethod
    def create(
            cls,
            id: str,
            object_type: str,
            owner_id: str,
            who_has_access: str | None = None,
            link_access: str | None = None
    ) -> 'InstanceAccessProfile':
        def create_instance_access_profile() -> 'InstanceAccessProfile':
            data: dict[str, any] = {"id": id, "object_type": object_type, "owner_id": owner_id}
            if who_has_access is not None:
                validate_enum_value(who_has_access, WhoHasAccessEnum)
                data["who_has_access"] = who_has_access
            if link_access is not None:
                validate_enum_value(link_access, LinkAccessEnum)
                data["link_access"] = link_access
            api_response: Response = signed_requests.request(
                method="POST",
                url=f"{constants.ACCESS_BASE_URL}"
                    f"{constants.ACCESS_CREATE_INSTANCE_ACCESS_PROFILE_ENDPOINT}",
                json=data
            )
            if api_response.status_code == 201:
                return cls(**api_response.json())
            raise InfuzuError(f"Error creating instance access profile: {api_response.text}")
        return INSTANCE_ACCESS_PROFILE_CACHE.get(
            cache_key_name=f'{id}', specialized_fetch_function=create_instance_access_profile
        )

    @classmethod
    def retrieve(cls, id: str) -> 'InstanceAccessProfile':
        def get_instance_access_profile() -> 'InstanceAccessProfile':
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.ACCESS_BASE_URL}"
                    f"{constants.ACCESS_RETRIEVE_INSTANCE_ACCESS_PROFILE_ENDPOINT}"
                .replace('<str:instance_id>', id)
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            raise InfuzuError(f"Error retrieving instance access profile: {api_response.text}")
        return INSTANCE_ACCESS_PROFILE_CACHE.get(
            cache_key_name=f'{id}', specialized_fetch_function=get_instance_access_profile
        )

    @classmethod
    def delete(cls, id: str) -> bool:
        def delete_instance_access_profile() -> bool:
            api_response: Response = signed_requests.request(
                method="DELETE",
                url=f"{constants.ACCESS_BASE_URL}"
                    f"{constants.ACCESS_DELETE_INSTANCE_ACCESS_PROFILE_ENDPOINT}"
                .replace('<str:instance_id>', id)
            )
            if api_response.status_code == 204:
                return True
            raise InfuzuError(f"Error creating instance access profile: {api_response.text}")
        return INSTANCE_ACCESS_PROFILE_CACHE.get(
            cache_key_name=f'delete__{id}',
            specialized_fetch_function=delete_instance_access_profile,
            specialized_expiry_time=1
        )
