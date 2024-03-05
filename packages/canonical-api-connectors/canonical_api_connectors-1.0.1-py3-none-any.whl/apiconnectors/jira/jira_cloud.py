"""Jira Cloud API client."""

# pylint: disable=W0212

from functools import lru_cache

from jira import (
    JIRA,
    exceptions as jira_errors,
)
from jira.utils import json_loads


class JiraCloudAPI:
    """
    JiraCloudAPI - Class for interacting with the Jira Cloud API.

    This class provides a Python interface for interacting with the Jira Cloud API.
    It allows performing various administrative tasks such as user management,
    group membership clearing, and other operations.

    Attributes:
        api_user (str): The username or email address used for authentication.
        api_token (str): The API token associated with the specified user for authentication.
        api_root (str): The root URL of the Jira Cloud API.

    Exceptions:
        APIError: Base Jira API error.
        UserNotFoundError (APIError): Exception raised when a user is not found.
        GroupMembershipClearingError (APIError): Exception raised when clearing user group memberships fails.

    Usage:
    ```python
    jira_cloud = JiraCloudAPI(api_user="<user>", api_token="<token>", api_root="<root>")
    jira_cloud.get_user("<email>")
    ```
    """

    class APIError(Exception):
        """Base Jira API error."""

    class UserNotFoundError(APIError):
        """Exception raised when a user is not found."""

    class JiraPermissionError(APIError):
        """Exception raised when there is a permission error during Jira operations."""

    def __init__(self, api_user, api_token, api_root):
        """
        Initialize an instance of the JiraCloudAPI class for interacting with the Jira Cloud API.

        Args:
            api_user (str): The username or email address for authentication with the Jira Cloud API.
            api_token (str): The API token associated with the specified user for authentication.
            api_root (str): The root URL of the Jira Cloud API.

        Attributes:
            api_user (str): The username or email address used for authentication.
            api_token (str): The API token associated with the specified user for authentication.
            api_root (str): The root URL of the Jira Cloud API.
        """
        self.api_user = api_user
        self.api_token = api_token
        self.api_root = api_root
        self._authorize()

    def _authorize(self):
        """Connect and authenticate to JIRA."""
        self.jira = JIRA(self.api_root, basic_auth=(self.api_user, self.api_token))

    def add_user(
        self, email, firstname, lastname, notify=True, ignore_existing=False
    ) -> bool:
        """
        Add a user to Jira.

        This method adds a new user to Jira with the specified email, firstname, and lastname.

        Args:
            email (str): The email address of the user to be added.
            firstname (str): The first name of the user.
            lastname (str): The last name of the user.
            notify (bool, optional): Whether to send a notification to the user upon addition (default is True).
            ignore_existing (bool, optional): Whether to ignore existing users (default is False).

        Returns:
            bool: True if the user is successfully added, False otherwise.
        """
        fullname = f"{firstname} {lastname}"
        return self.jira.add_user(
            username=email,
            email=email,
            fullname=fullname,
            notify=notify,
            ignore_existing=ignore_existing,
        )

    @lru_cache
    def get_user(self, email):
        """
        Fetch user information from Jira.

        Args:
            email (str): The email address of the user to be fetched.

        Returns:
            jira.resources.User: A Jira User object containing information about the requested user.

        Raises:
            UserNotFoundError: If no user is found with the specified email address.
            APIError: If multiple users are found with the specified email address or if user information is
            inconsistent.
        """
        # Jira Cloud does not allow for querying inactive users per the API docs.
        # https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-user-search/#api-rest-api-2-user-search-get
        users = self.jira.search_users(maxResults=5, query=email)
        if len(users) == 0:
            raise self.UserNotFoundError(
                f"Cannot find account matching email={email}, were they just added ?"
            )

        if len(users) > 1:
            raise self.APIError(f"Multiple users found with email={email}")

        user = users[0]
        # Usually there is no email entry, but if present, check it.
        if user.emailAddress and user.emailAddress != email:
            raise self.APIError(
                f"Found user email ({user.emailAddress}) does not match requested email ({email})."
            )
        return user

    def list_user_groups(self, email):
        """
        List all groups that a user is a member of in Jira.

        Args:
            email (str): The email address of the user whose groups are to be listed.

        Returns:
            dict: A dictionary containing group information with group ID as the key and group name as the value.

        Raises:
            UserNotFoundError: If the specified user cannot be found in Jira.
        """
        user = self.get_user(email)
        if not user:
            raise self.UserNotFoundError(
                f"Cannot find account matching email={email}. If they were just added, there might be a small delay until they are available."
            )

        url = user._get_url("user/groups")
        params = {"accountId": user.accountId}
        r = user._session.get(url, headers={}, params=params)
        j = json_loads(r)
        return {group["groupId"]: group["name"] for group in j}

    def delete_user(self, email) -> bool:
        """
        Remove a user from Jira.

        Args:
            email (str): The email address of the user to be deleted.

        Returns:
            bool: True if the user is successfully deleted, False otherwise.

        Raises:
            UserNotFoundError: If the specified user cannot be found in Jira.
        """
        user = self.get_user(email)
        if not user.accountId:
            raise self.UserNotFoundError("Unable to find user accountId.")
        # XXX This is a workaround until accountId is fully supported
        # XXX See: https://github.com/pycontribs/jira/issues/1241 is resolved
        username = f"{email}&accountId={user.accountId}"
        return self.jira.delete_user(username=username)

    def search_issues(self, issue_filter) -> list:
        """
        Search for Jira issues based on the provided JQL filter.

        Args:
            issue_filter (str): The JQL filter to search for issues.

        Returns:
            list: A list of Jira issues matching the provided filter.

        Raises:
            ValueError: If attempting to fetch more issues than reported by Jira.

        Notes:
            - The search is performed iteratively to handle cases where the number of matching issues exceeds
            the maximum allowed results per query.
        """
        found = []
        start_at = 0
        first = True
        max_results = 100
        issues = None
        while first or issues.maxResults:
            first = False
            issues = self.jira.search_issues(
                jql_str=issue_filter, maxResults=max_results, startAt=start_at
            )
            found.extend(issues)
            if len(found) >= issues.total:
                break
            start_at += issues.maxResults
            if start_at > issues.total:
                raise ValueError(
                    f"Trying to fetch more issues {start_at} than reported by Jira {issues.total}"
                )
        return found

    def unassign_issues(self, from_address):
        """
        Unassign issues in Jira assigned to a specified user.

        Args:
            from_address (str): The email address or username of the user whose assigned issues should be unassigned.

        Raises:
            ValueError: If 'from_address' is not provided.
        """
        if not from_address:
            raise ValueError("Unable to search for issues without a from_address")
        issues = self.search_issues(f'assignee = "{from_address}"')
        issues_text = [issue.key for issue in issues]
        issues_text = " ".join(issues_text)

        permission_denied_errors = []
        other_errors = []
        for issue in issues:
            try:
                self.jira.assign_issue(issue, None)
            except jira_errors.JIRAError as e:
                if e.text == "You do not have permission to assign issues.":
                    permission_denied_errors.append(issue.key)
                    continue

                other_errors.append(issue.key)
        if permission_denied_errors:
            raise self.JiraPermissionError(
                f"Permission error while unassigning: {' '.join(permission_denied_errors)}"
            )

        if other_errors:
            raise ValueError(
                f"Unknown error while unassigning: {' '.join(other_errors)}"
            )

    # flake8: noqa: C901
    def update_issues_reporter(self, from_address, to_address, notify=False):
        """
        Update the reporter of Jira issues from one user to another.

        Args:
            from_address (str): The email address of the current reporter.
            to_address (str): The email address of the new reporter.
            notify (bool): Whether or not to send a notification for each issue update.

        Raises:
            ValueError: If 'from_address' or 'to_address' is not provided.
            UserNotFoundError: If 'to_address' user is not found.
            JiraPermissionError: If there is a permission error during the issue update.
        """
        if not from_address:
            raise ValueError("Unable to search for issues without a from_address")
        if not to_address:
            raise ValueError(
                "Unable to update issues reporter to nobody, please set to_address"
            )

        update_to_user = self.get_user(to_address)
        if not update_to_user:
            raise self.UserNotFoundError(
                f"Cannot find account matching email={to_address}. If they were just added, there might be a small delay until they are available."
            )

        issues = self.search_issues(f'reporter = "{from_address}"')
        issues_text = [issue.key for issue in issues]
        issues_text = " ".join(issues_text)

        permission_denied_errors = []
        other_errors = []
        for issue in issues:
            try:
                issue.update(
                    notify=notify,
                    fields={"reporter": {"accountId": update_to_user.accountId}},
                )
            except jira_errors.JIRAError as e:
                if e.text == "You do not have permission to update issues.":
                    permission_denied_errors.append(issue.key)
                    continue
                if "Field 'reporter' cannot be set" in e.text:
                    permission_denied_errors.append(issue.key)
                    continue

                other_errors.append(issue.key)
        if permission_denied_errors:
            raise self.JiraPermissionError(
                f"Permission error while updating reporter for: {' '.join(permission_denied_errors)}"
            )

        if other_errors:
            raise ValueError(
                f"Unknown error while updating reporter for: {' '.join(other_errors)}"
            )
