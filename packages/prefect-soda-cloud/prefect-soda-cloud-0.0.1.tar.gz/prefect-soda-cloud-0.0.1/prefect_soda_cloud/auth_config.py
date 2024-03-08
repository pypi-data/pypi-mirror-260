"""
This blocks can be used to store credentials
that will be used to authenticate to Soda Cloud APIs.
"""

from logging import Logger
from typing import Optional

from prefect.blocks.core import Block
from pydantic import Field, SecretStr, validator

from prefect_soda_cloud.soda_cloud_client import SodaCloudClient


class SodaCloudCredentials(Block):
    """
    This block contains sensitive informations
    that will be used during the authentication flow
    with Soda Cloud.
    Please refer to
    [Soda Cloud docs](https://docs.soda.io/api-docs/public-cloud-api-v1.html#/operations/GET/api/v1/test-login)
    for more information about authentication.

    Attributes:
        user_or_api_key_id: Username or API Key ID.
        pwd_or_api_key_secret: Password or API Key Secret.

    Example:
    ```python
    from prefect_soda_cloud import SodaCloudCredentials

    creds = SodaCloudCredentials(
        user_or_api_key_id="user",
        pwd_or_api_key_secret="pwd"
    )
    ```
    """  # noqa: E501

    _block_type_name = "Soda Cloud Credentials"
    _logo_url = "https://avatars.githubusercontent.com/u/45313710?s=200&v=4"  # noqa
    _documentation_url = "https://AlessandroLollo.github.io/prefect-soda-cloud/blocks/#prefect-soda-cloud.auth_config.SodaCloudCredentials"  # noqa

    user_or_api_key_id: str = Field(
        name="Username or API Key ID",
        default=None,
        description="Soda Cloud username or API Key ID.",
    )
    pwd_or_api_key_secret: SecretStr = Field(
        name="Password or API Key Secret",
        description="Soda Cloud password or API Key Secret.",
    )


class SodaCloudAuthConfig(Block):
    """
    This block can be used to store the configuration details
    required to interact with Soda Cloud and its APIs.

    Attributes:
        api_base_url: Soda Cloud base URL.
        creds: `SodaCloudCredentials` that
            will be used to authenticate to Soda Cloud.
        wait_secs_between_api_calls: The number of seconds to
            wait between API calls. Default to `10`. Must be >= 0.

    Example:
    ```python
    from prefect_soda_cloud import (
        SodaCloudAuthConfig,
        SodaCloudCredentials
    )

    auth_config = SodaCloudAuthConfig(
        api_base_url="https://cloud.soda.io",
        creds=SodaCloudCredentials(
            user_or_api_key_id="user",
            pwd_or_api_key_secret="pwd"
        ),
        wait_secs_between_api_calls=1
    )
    ```
    """

    _block_type_name = "Soda Cloud Auth Config"
    _logo_url = "https://avatars.githubusercontent.com/u/45313710?s=200&v=4"  # noqa
    _documentation_url = "https://AlessandroLollo.github.io/prefect-soda-cloud/blocks/#prefect-soda-cloud.auth_config.SodaCloudAuthConfig"  # noqa

    api_base_url: str = Field(
        name="Soda Cloud Base API URL",
        default="https://cloud.soda.io",
        description="Soda Cloud Base API URL.",
    )
    creds: SodaCloudCredentials
    wait_secs_between_api_calls: Optional[int] = Field(
        name="Wait time between API calls",
        default=10,
        description="Wait time in seconds between API calls. Must be >=0.",
    )

    @validator("wait_secs_between_api_calls")
    def _validate_wait_secs_between_api_calls(cls, value: int) -> int:
        """
        TODO
        """
        if value < 0:
            raise ValueError("wait_secs_between_api_calls must be >= 0")
        return value

    def get_client(self, logger: Logger) -> SodaCloudClient:
        """
        Returns a `SodaCloudClient` object.

        Args:
            logger (Logger): A configured logger.

        Returns:
            A `SodaCloudClient` object.
        """
        return SodaCloudClient(
            api_base_url=self.api_base_url,
            username=self.creds.user_or_api_key_id,
            password=self.creds.pwd_or_api_key_secret.get_secret_value(),
            logger=logger,
            wait_secs_between_api_calls=self.wait_secs_between_api_calls,
        )
