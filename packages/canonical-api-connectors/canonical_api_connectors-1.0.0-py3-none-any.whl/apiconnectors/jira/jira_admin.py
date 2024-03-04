"""Jira Admin API client."""

from enum import Enum
from functools import cached_property
import json

import requests


class HttpMethod(Enum):
    """Enum of API call types."""

    GET = "get"
    POST = "post"
    DELETE = "delete"


# See https://developer.atlassian.com/cloud/admin/organization/rest/
ADMIN_API_ROOT = "https://api.atlassian.com/admin"


class JiraAdminAPI:
    """
    JiraAdminAPI - Class for interacting with the Jira Admin API.

    This class provides a Python interface for interacting with the Jira Admin API.
    It allows performing various administrative tasks such as user management,
    group membership clearing, and other operations.

    Attributes:
        admin_api_root (str): The root URL of the Jira Admin API.
        admin_api_key (str): The API key for authentication with the Jira Admin API.
        org_id (str or None): The organization ID obtained from the Jira Admin API.
        _requests (Session): The requests session for making HTTP requests to the Jira Admin API.

    Exceptions:
        APIError: Base Jira API error.
        UserNotFoundError (APIError): Exception raised when a user is not found.
        GroupMembershipClearingError (APIError): Exception raised when clearing user group memberships fails.

    Usage:
    ```python
    jira_admin = JiraAdminAPI(admin_api_key="your_api_key")
    jira_admin.suspend_managed_user("<email>")
    ```
    """

    class APIError(Exception):
        """Base Jira API error."""

    class UserNotFoundError(APIError):
        """Exception raised when a user is not found."""

    class GroupMembershipClearingError(APIError):
        """Exception raised when clearing user group memberships fails."""

    def __init__(self, admin_api_key, admin_api_root=ADMIN_API_ROOT):
        """
        Initialize an instance of the JiraAdminAPI class for interacting with the Admin API.

        Args:
            admin_api_key (str): The API key for authentication with the Admin API.
            admin_api_root (str, optional): The root URL of the Admin API.

        Attributes:
            admin_api_root (str): The root URL of the Admin API.
            admin_api_key (str): The API key for authentication with the Admin API.
            org_id (str or None): The organization ID obtained from the Admin API.
            _requests (Session): The requests session for making HTTP requests to the Admin API.
        """
        self.admin_api_root = admin_api_root
        self.admin_api_key = admin_api_key
        self._requests = requests.sessions.Session()

    def admin_api_call(
        self,
        url,
        method: HttpMethod,
        data=None,
        params=None,
        handled_codes=None,
        extract_data=False,
        decode_json=True,
    ):
        """
        Perform an Admin API call and return the HTTP status code and JSON result data.

        Args:
            url (str): The URL for the API call.
            method (HttpMethod): The HTTP method for the API call (e.g., HttpMethod.GET).
            data (dict, optional): The data to include in the request body.
            params (dict, optional): The parameters to include in the request URL.
            handled_codes (list, optional): List of HTTP status codes to be treated as successful responses.
            extract_data (bool, optional): Whether to extract and return data from the response.
            decode_json (bool, optional): Whether to decode the response content as JSON.

        Returns:
            tuple: A tuple containing the HTTP status code and the result of the API call.

        Raises:
            ValueError: If the API call result is missing the expected 'data' attribute.
        """
        headers = {
            "Authorization": f"Bearer {self.admin_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        url = f"{self.admin_api_root}{url}"
        callback = getattr(self._requests, method.value)
        if data:
            data = json.dumps(data)

        next_pagination_link = url
        result = []
        while next_pagination_link:
            response = callback(
                next_pagination_link,
                allow_redirects=False,
                headers=headers,
                data=data,
                params=params,
            )
            if not handled_codes or response.status_code not in handled_codes:
                response.raise_for_status()

            if decode_json:
                try:
                    json_r = response.json()
                except requests.exceptions.JSONDecodeError as e:
                    raise ValueError("Admin API returned an invalid JSON result") from e
            else:
                return response.status_code, response

            if not extract_data:
                return response.status_code, json_r
            if "data" not in json_r:
                raise ValueError(
                    f"API call for {url} is missing expected `data` attribute: {json_r}"
                )
            result.extend(json_r["data"])
            next_pagination_link = json_r.get("links", {}).get("next")
        return response.status_code, result

    @cached_property
    def org_id(self):
        """
        Get the organization ID from the admin API and set the org_id attribute.

        Raises:
            ValueError: If the API response does not contain exactly one organization ID.
        """
        url = "/v1/orgs"
        status, result = self.admin_api_call(
            url, method=HttpMethod.GET, extract_data=True
        )
        if len(result) != 1:
            raise ValueError(
                f"Could not determine Atlassian Org, did not get exactly one: {result}"
            )
        org = result[0]
        return org["id"]

    @cached_property
    def all_users(self):
        """
        Retrieve all users in the organization from the admin API.

        This property returns a list of all users in the organization obtained from the admin API.
        The result is cached for subsequent calls, improving performance.

        Returns:
            list: A list containing user details retrieved from the admin API.

        Raises:
            ValueError: If the organization ID is not set.
        """
        url = f"/v1/orgs/{self.org_id}/users"
        _, result = self.admin_api_call(url, method=HttpMethod.GET, extract_data=True)
        return result

    def get_managed_user_account_id(self, email):
        """
        Return the Atlassian account ID for a managed user.

        Args:
            email (str): The email address of the managed user.

        Returns:
            str or None: The Atlassian account ID of the managed user if found,
            or None if no user matches the provided email address.

        Raises:
            ValueError: If the admin API returns a user entry without an account ID.
        """
        user_info = self.get_managed_user_info(email)
        if not user_info:
            return None

        account_id = user_info.get("account_id")
        if not account_id:
            raise ValueError(
                f"Admin API returned a user entry without accountId: {user_info}"
            )

        return account_id

    def get_managed_user_info(self, email):
        """
        Return details for a managed user in the Atlassian directory.

        Args:
            email (str): The email address of the managed user.

        Returns:
            dict or None: A dictionary containing the details of the managed user if found,
            or None if no user matches the provided email address.

        Raises:
            ValueError: If multiple users are found with the same email address.
        """
        # Interesting attributes are access_billable, account_id, account_status, product_access
        # Although account_status does not seem to match suspended/active status
        found = [user for user in self.all_users if user.get("email") == email]
        if not found:
            return None
        if len(found) > 1:
            raise ValueError(
                f"Found more than one user matching email address {email}: {found}"
            )

        return found[0]

    def clear_group_membership(self, email, groups):
        """
        Clear a managed user account's group memberships per listed group ids.

        Args:
            email (str): The email address of the user whose group memberships need to be cleared.
            groups (dict): A dictionary where keys are group IDs and values are group names.

        Raises:
            GroupMembershipClearingError: If clearing the user's membership from any group fails.
        """
        account_id = self.get_managed_user_account_id(email)
        groups_text = [f"{gname} ({gid})" for gid, gname in groups.items()]
        groups_text = ", ".join(groups_text)
        for group_id, group in groups.items():
            url = f"/v1/orgs/{self.org_id}/directory/groups/{group_id}/memberships/{account_id}"
            status, result = self.admin_api_call(
                url, method=HttpMethod.DELETE, handled_codes=[200]
            )
            if status != 200:
                raise self.GroupMembershipClearingError

    def suspend_managed_user(self, email) -> bool:
        """
        Suspend a managed user account.

        Suspending a managed account will not remove it from the organization but free up seats and prevent login.
        This will also keep group memberships for easy restoration.

        Args:
            email (str): The email address of the managed user to be suspended.

        Returns:
            bool: True if the user account was successfully suspended, False otherwise.

        Raises:
            UserNotFoundError: If no user is found with the provided email address.
        """
        account_id = self.get_managed_user_account_id(email)
        url = f"/v1/orgs/{self.org_id}/directory/users/{account_id}/suspend-access"
        status, result = self.admin_api_call(
            url, method=HttpMethod.POST, handled_codes=[200, 404]
        )
        if status == 404:
            raise self.UserNotFoundError

        return status == 200

    def unsuspend_managed_user(self, email, account_id) -> bool:
        """
        Restore access to a suspended managed user account.

        Args:
            email (str): The email address of the suspended managed user.
            account_id (str): The Atlassian account ID of the suspended managed user.

        Returns:
            bool: True if the user account was successfully unsuspended, False otherwise.

        Raises:
            UserNotFoundError: If no user is found with the provided email address.
        """
        url = f"/v1/orgs/{self.org_id}/directory/users/{account_id}/restore-access"
        status, result = self.admin_api_call(
            url, method=HttpMethod.POST, handled_codes=[200, 404]
        )
        if status == 404:
            raise self.UserNotFoundError

        return status == 200

    def delete_managed_user(self, email) -> bool:
        """
        Delete a managed user account.

        Args:
            email (str): The email address of the managed user.

        Returns:
            bool: True if the user account was successfully deleted, False otherwise.

        Raises:
            UserNotFoundError: If no user is found with the provided email address.
            ValueError: If the admin API returns a user entry without an accountId.
        """
        user_info = self.get_managed_user_info(email)
        if not user_info:
            raise self.UserNotFoundError

        account_id = user_info.get("account_id")
        if not account_id:
            raise ValueError(
                f"Unable to delete user, Admin API returned a user entry without accountId: {user_info}",
            )
        url = f"/v1/orgs/{self.org_id}/directory/users/{account_id}"
        status, result = self.admin_api_call(
            url, method=HttpMethod.DELETE, handled_codes=[204], decode_json=False
        )
        return status == 204
