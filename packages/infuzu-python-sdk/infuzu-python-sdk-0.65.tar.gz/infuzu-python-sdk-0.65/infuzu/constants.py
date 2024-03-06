"""
constants.py
This module contains constant values used throughout the SDK for making requests
to the associated API and other related operations.
"""
import os

# The header name used to send the authentication token with API requests.
INFUZU_AUTH_TOKEN_HEADER_NAME: str = os.environ.get('INFUZU_AUTH_TOKEN_HEADER_NAME', "I-Auth-Token")

# Default timeout for API requests in seconds.
DEFAULT_REQUEST_TIMEOUT: int = os.environ.get('DEFAULT_REQUEST_TIMEOUT', 30)

# Base URL for the Clockwise service hosted by Infuzu.
CLOCKWISE_BASE_URL: str = os.environ.get("CLOCKWISE_BASE_URL", "https://clockwise.infuzu.com/")

# Endpoint to retrieve assignments from the Clockwise service.
CLOCKWISE_RETRIEVE_ASSIGNMENT_ENDPOINT: str = os.environ.get('CLOCKWISE_RETRIEVE_ASSIGNMENT_ENDPOINT', "assignment/")

# Endpoint to mark an assignment as completed in the Clockwise service.
CLOCKWISE_ASSIGNMENT_COMPLETE_ENDPOINT: str = os.environ.get(
    'CLOCKWISE_ASSIGNMENT_COMPLETE_ENDPOINT', "task-completed/"
)
CLOCKWISE_CREATE_RULE_ENDPOINT: str = os.environ.get('CLOCKWISE_CREATE_RULE_ENDPOINT', "rule/create/")
CLOCKWISE_DELETE_RULE_ENDPOINT: str = os.environ.get('CLOCKWISE_DELETE_RULE_ENDPOINT', "rule/delete/<str:rule_id>/")
CLOCKWISE_RULE_LOGS_ENDPOINT: str = os.environ.get('CLOCKWISE_RULE_LOGS_ENDPOINT', "rule/logs/<str:rule_id>/")


INFUZU_KEYS_BASE_URL: str = os.environ.get("INFUZU_KEYS_BASE_URL", "https://keys.infuzu.com/")
INFUZU_KEYS_KEY_PAIR_ENDPOINT: str = os.environ.get("INFUZU_KEYS_KEY_PAIR_ENDPOINT", "api/key/<str:key_id>/")


COGITOBOT_BASE_URL: str = os.environ.get("COGITOBOT_BASE_URL", "https://cogitobot.infuzu.com/")
COGITOBOT_RETRIEVE_DOCUMENT_VERSION_ENDPOINT: str = os.environ.get(
    "COGITOBOT_RETRIEVE_DOCUMENT_VERSION_ENDPOINT",
    "internal/document-version/<str:document_version_id>/"
)


ACCESS_BASE_URL: str = os.environ.get("ACCESS_BASE_URL", "https://accounts.infuzu.com/")
ACCESS_RETRIEVE_OBJECT_ACCESS_PROFILE_ENDPOINT: str = os.environ.get(
    "ACCESS_RETRIEVE_OBJECT_ACCESS_PROFILE_ENDPOINT", 'access/object-access-profile/<str:user_id>/<str:object_type>/'
)
ACCESS_RETRIEVE_USER_ACCESS_PROFILE_ENDPOINT: str = os.environ.get(
    "ACCESS_RETRIEVE_USER_ACCESS_PROFILE_ENDPOINT", 'access/user-access-profile/<str:user_id>/'
)
DEFAULT_ACCESS_INSTANCE_ACCESS_PROFILE_ENDPOINT: str = os.environ.get(
    'DEFAULT_ACCESS_INSTANCE_ACCESS_PROFILE_ENDPOINT', 'access/instance-access-profile/'
)
ACCESS_CREATE_INSTANCE_ACCESS_PROFILE_ENDPOINT: str = os.environ.get(
    "ACCESS_CREATE_INSTANCE_ACCESS_PROFILE_ENDPOINT", DEFAULT_ACCESS_INSTANCE_ACCESS_PROFILE_ENDPOINT
)
ACCESS_RETRIEVE_INSTANCE_ACCESS_PROFILE_ENDPOINT: str = os.environ.get(
    "ACCESS_RETRIEVE_INSTANCE_ACCESS_PROFILE_ENDPOINT",
    DEFAULT_ACCESS_INSTANCE_ACCESS_PROFILE_ENDPOINT + '<str:instance_id>/'
)
ACCESS_DELETE_INSTANCE_ACCESS_PROFILE_ENDPOINT: str = os.environ.get(
    "ACCESS_DELETE_INSTANCE_ACCESS_PROFILE_ENDPOINT",
    DEFAULT_ACCESS_INSTANCE_ACCESS_PROFILE_ENDPOINT + '<str:instance_id>/'
)

SUBSCRIPTIONS_BASE_URL: str = os.environ.get("SUBSCRIPTIONS_BASE_URL", "https://accounts.infuzu.com/")
SUBSCRIPTIONS_RETRIEVE_SUBSCRIPTIONS: str = os.environ.get(
    "SUBSCRIPTIONS_RETRIEVE_SUBSCRIPTIONS", 'subscriptions/subscriptions/'
)
SUBSCRIPTIONS_RETRIEVE_SUBSCRIPTION: str = os.environ.get(
    "SUBSCRIPTIONS_RETRIEVE_SUBSCRIPTION", 'subscriptions/subscription/<str:subscription_id>/'
)
SUBSCRIPTIONS_RETRIEVE_SUBSCRIPTION_FREE_TRIAL: str = os.environ.get(
    "SUBSCRIPTIONS_RETRIEVE_SUBSCRIPTION_FREE_TRIAL",
    'subscriptions/subscription-free-trial/<str:subscription_id>/<str:user_id>/'
)
SUBSCRIPTIONS_CREATE_SUBSCRIPTION_FREE_TRIAL: str = os.environ.get(
    "SUBSCRIPTIONS_CREATE_SUBSCRIPTION_FREE_TRIAL",
    'subscriptions/subscription-free-trial/<str:subscription_id>/<str:user_id>/'
)
SUBSCRIPTIONS_SUBSCRIBE_TO_PLAN: str = os.environ.get(
    "SUBSCRIPTIONS_SUBSCRIBE_TO_PLAN", 'subscriptions/plan/<str:subscription_plan_id>/subscribe/<str:user_id>/'
)
SUBSCRIPTIONS_RETRIEVE_USER_SUBSCRIPTIONS: str = os.environ.get(
    "SUBSCRIPTIONS_RETRIEVE_USER_SUBSCRIPTIONS", 'subscriptions/user-subscriptions/'
)
SUBSCRIPTIONS_CREATE_USER_SUBSCRIPTION: str = os.environ.get(
    "SUBSCRIPTIONS_CREATE_USER_SUBSCRIPTION", 'subscriptions/user-subscriptions/'
)
SUBSCRIPTIONS_RETRIEVE_USER_SUBSCRIPTION: str = os.environ.get(
    "SUBSCRIPTIONS_RETRIEVE_USER_SUBSCRIPTION", 'subscriptions/user-subscription/<str:user_subscription_id>/'
)
