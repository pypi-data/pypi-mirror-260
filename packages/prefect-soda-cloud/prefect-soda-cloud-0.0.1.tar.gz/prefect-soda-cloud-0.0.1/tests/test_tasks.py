from urllib.parse import urljoin

import pytest
import responses
from prefect import flow

from prefect_soda_cloud import SodaCloudAuthConfig, SodaCloudCredentials
from prefect_soda_cloud.exceptions import TriggerScanException
from prefect_soda_cloud.tasks import trigger_scan

creds = SodaCloudCredentials(user_or_api_key_id="test", pwd_or_api_key_secret="test")

auth_config = SodaCloudAuthConfig(
    api_base_url="https://test.test", creds=creds, wait_secs_between_api_calls=1
)


@responses.activate
def test_trigger_scan_fails():
    api_base_url = "https://test.test"
    trigger_scan_endpoint = "api/v1/scans"
    url = urljoin(api_base_url, trigger_scan_endpoint)

    @flow(name="trigger_scan_fails")
    def test_flow():
        return trigger_scan(
            scan_name="test_scan",
            soda_cloud_auth_config=auth_config,
            data_timestamp=None,
        )

    responses.add(responses.POST, url, status=500, json={"error": "Error!"})

    with pytest.raises(TriggerScanException, match=str({"error": "Error!"})):
        test_flow()


@responses.activate
def test_trigger_scan_succeed():
    api_base_url = "https://test.test"
    trigger_scan_endpoint = "api/v1/scans"
    url = urljoin(api_base_url, trigger_scan_endpoint)

    @flow(name="trigger_scan_succeed")
    def test_flow():
        return trigger_scan(
            scan_name="test_scan",
            soda_cloud_auth_config=auth_config,
            data_timestamp=None,
        )

    responses.add(responses.POST, url, status=201, headers={"X-Soda-Scan-Id": "abc"})

    result = test_flow()
    assert result == "abc"
