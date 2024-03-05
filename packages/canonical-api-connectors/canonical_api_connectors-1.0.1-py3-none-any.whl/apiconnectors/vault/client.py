"""Vault client."""

import datetime
import sys

import dateutil.parser
import hvac
import requests.exceptions


def _validate_data_format(data):
    return "secret_id" in data["data"] and "secret_id_accessor" in data["data"]


class VaultManager:
    """Manages interactions with HashiCorp Vault.

    Attributes:
        vault_addr (str): The address of the HashiCorp Vault instance.
        token (str): Token used for authentication.
        ldap_username (str): LDAP username for authentication.
        ldap_password (str): LDAP password for authentication.
        role_id (str): Role ID for authentication.
        secret_id (str): Secret ID for authentication.
        client (VaultClient): The Vault client for interacting with the Vault.

    Exceptions:
        VaultIsNotAuthenticatedError (Exception): Raised when the vault is not authenticated.
        VaultUnwrappingError (ValueError): Raised when there is an error in unwrapping vault secrets.
        VaultExpireCheckError (Exception): Raised when there is an error in checking vault expiration.
        VaultGenerateSecretError (Exception): Raised when there is an error generating a vault secret.
        VaultSecretIdExpiredError (PermissionError): Raised when the secret ID has expired.
    """

    class VaultIsNotAuthenticatedError(Exception):
        """Vault is not authenticated.  Check environment setup."""

    class VaultUnwrappingError(ValueError):
        """Error in unwrapping vault secrets."""

    class VaultExpireCheckError(Exception):
        """Error in checking vault expiration."""

    class VaultGenerateSecretError(Exception):
        """Error generating a vault secret."""

    class VaultSecretIdExpiredError(PermissionError):
        """Secret ID has expired."""

    def __init__(
        self,
        vault_addr=None,
        token=None,
        ldap_username=None,
        ldap_password=None,
        role_id=None,
        secret_id=None,
    ):
        """Initialize VaultManager with authentication details.

        Args:
            vault_addr (str): The address of the HashiCorp Vault instance.
            token (str): Token used for authentication.
            ldap_username (str): LDAP username for authentication.
            ldap_password (str): LDAP password for authentication.
            role_id (str): Role ID for authentication.
            secret_id (str): Secret ID for authentication.
        """
        self.vault_addr = vault_addr
        self.token = token
        self.ldap_username = ldap_username
        self.ldap_password = ldap_password
        self.role_id = role_id
        self.secret_id = secret_id
        self.client = self.get_vault_client()

    # flake8: noqa: C901
    def get_vault_client(self):
        """Return an authenticated Vault client."""
        if not self.vault_addr:
            raise RuntimeError("Missing Vault address")

        client = hvac.Client(
            url=self.vault_addr,
        )

        if self.token:
            client.token = self.token
        elif self.ldap_username and self.ldap_password:
            try:
                client.auth.ldap.login(
                    username=self.ldap_username,
                    password=self.ldap_password,
                )
            except requests.exceptions.ConnectionError as e:
                raise e
        elif self.role_id and self.secret_id:
            try:
                client.auth.approle.login(
                    role_id=self.role_id,
                    secret_id=self.secret_id,
                )
            except hvac.exceptions.InvalidRequest as e:
                if "invalid secret id" in str(e):
                    raise self.VaultSecretIdExpiredError from e
                raise e
        else:
            raise RuntimeError("Missing authentication method parameters.")

        if not client.is_authenticated():
            raise self.VaultIsNotAuthenticatedError(
                "Vault is not authenticated, but login succeeded! Something is very wrong."
            )

        return client

    def unwrap_vault_secret(self, wrapped_secret):
        """
        Unwrap a vault secret to retrieve its contents.

        Args:
            wrapped_secret (str): The wrapped secret token to be unwrapped.

        Returns:
            dict: A dictionary containing the unwrapped secrets.

        Raises:
            VaultUnwrappingError: If the unwrapping process does not yield the expected values or data format.
        """
        unwrapping_client = hvac.Client(url=self.vault_addr, token=wrapped_secret)

        try:
            unwrap_response = unwrapping_client.sys.unwrap()
            if not _validate_data_format(unwrap_response):
                raise self.VaultUnwrappingError(
                    "Unwrapping secret did not yield expected values"
                )
            return unwrap_response["data"]
        except KeyError as e:
            raise self.VaultUnwrappingError(
                "Unwrapping secret did not yield expected data format"
            ) from e

    def check_auth_expiration(self, role_name, min_expire_seconds=3600):
        """
        Check the expiration status of an authentication secret.

        Args:
            role_name (str): The name of the Vault AppRole for which the secret is generated.
            min_expire_seconds (int): Minimum expiration time in seconds to consider when checking.

        Returns:
            bool: True if the authentication secret will expire in less than half its ttl, False otherwise.
                  If that value is lower than min_expire_seconds, use min_expire_seconds for threshold.

        Raises:
            VaultExpireCheckError: If reading Vault secret-id does not yield the expected data format or if
                                the Vault secret-id expiration_time has an unexpected date format.
        """
        # First let's extract expiration time.
        try:
            data = self.client.auth.approle.read_secret_id(
                role_name=role_name, secret_id=self.secret_id
            )
            expire_on = dateutil.parser.isoparse(data["data"]["expiration_time"])
        except KeyError as e:
            raise self.VaultExpireCheckError(
                "Reading Vault secret-id did not yield expected data format"
            ) from e
        except (ValueError, TypeError) as e:
            raise self.VaultExpireCheckError(
                "Vault secret-id expiration_time has an unexpected date format"
            ) from e

        # Now let's check against TTL or min_expire_seconds.
        now = datetime.datetime.now(datetime.timezone.utc)
        if expire_on < now:
            # Already expired
            return True
        delta = expire_on - now
        try:
            ttl = data["data"]["secret_id_ttl"]
            expire_seconds = max(min_expire_seconds, ttl / 2)
            return delta.seconds < expire_seconds
        except Exception:
            # If ttl based expiry fails, use min_expire_seconds
            return delta.seconds < min_expire_seconds

    def generate_secret_id(self, role_name):
        """
        Generate a new secret-id for a specified Vault AppRole.

        Args:
            role_name (str): The name of the Vault AppRole for which to generate a new secret-id.

        Returns:
            dict: A dictionary containing the newly generated secret-id information.

        Raises:
            VaultGenerateSecretError: If generating a new secret-id does not yield the expected data format.
        """
        try:
            data = self.client.auth.approle.generate_secret_id(role_name=role_name)
            if not _validate_data_format(data):
                raise self.VaultGenerateSecretError(
                    "Generating a new secret-id did not yield expected data format"
                )
            return data["data"]
        except KeyError as e:
            raise self.VaultGenerateSecretError(
                "Generating a new secret-id did not yield expected data format"
            ) from e
