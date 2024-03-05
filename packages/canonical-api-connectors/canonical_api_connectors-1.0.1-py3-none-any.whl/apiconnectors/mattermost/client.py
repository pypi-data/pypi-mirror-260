"""Mattermost client."""

from mattermostdriver import (
    Client,
    Driver,
)


class MattermostClient(Driver):
    """
    A class which wraps the `mattermostdriver.Driver` class.

    Attributes:
        options (dict): Configuration options for the Mattermost driver.
        client_cls (Client): Client class.

    Inherits:
        Driver: Base class for MattermostClient, providing common functionality.
    """

    # pylint: disable=W0246
    def __init__(
        self,
        options: dict,
        client_cls: Client = Client,
    ):
        """Initialize MattermostClient.

        Args:
            options (dict): Configuration options for the Mattermost driver.
            client_cls (Client): Client class.
        """
        super().__init__(options, client_cls)
