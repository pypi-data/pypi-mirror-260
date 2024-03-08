import pytest

from prefect_soda_cloud.auth_config import SodaCloudAuthConfig, SodaCloudCredentials


def test_credentials_construction():
    username = "test"
    password = "test"
    creds = SodaCloudCredentials(
        user_or_api_key_id=username, pwd_or_api_key_secret=password
    )

    assert creds.user_or_api_key_id == username
    assert creds.pwd_or_api_key_secret.get_secret_value() == password


def test_auth_config_construction_fails():
    username = "test"
    password = "test"
    creds = SodaCloudCredentials(
        user_or_api_key_id=username, pwd_or_api_key_secret=password
    )

    with pytest.raises(ValueError, match="wait_secs_between_api_calls must be >= 0"):
        SodaCloudAuthConfig(
            api_base_url="https://test.co", creds=creds, wait_secs_between_api_calls=-1
        )
