import logging
from urllib.parse import urljoin

import pytest
import responses

from prefect_soda_cloud.exceptions import (
    GetScanLogsException,
    GetScanStatusException,
    TriggerScanException,
)
from prefect_soda_cloud.soda_cloud_client import SodaCloudClient


def test_client_construction():
    expected_api_base_url = "https://foo.bar"
    expected_username = "user"
    expected_password = "password"
    expected_wait_secs_between_api_calls = 1

    client = SodaCloudClient(
        api_base_url=expected_api_base_url,
        username=expected_username,
        password=expected_password,
        wait_secs_between_api_calls=expected_wait_secs_between_api_calls,
        logger=logging.getLogger(),
    )

    assert client.api_base_url == expected_api_base_url
    assert client.wait_secs_between_api_calls == expected_wait_secs_between_api_calls


@responses.activate
def test_trigger_scan_fails():
    expected_api_base_url = "https://foo.bar"
    expected_trigger_scan_url = urljoin(expected_api_base_url, "api/v1/scans")
    expected_username = "user"
    expected_password = "password"
    expected_wait_secs_between_api_calls = 1
    expected_error = {"error": "Error!"}

    responses.add(
        responses.POST, expected_trigger_scan_url, status=500, json=expected_error
    )

    client = SodaCloudClient(
        api_base_url=expected_api_base_url,
        username=expected_username,
        password=expected_password,
        wait_secs_between_api_calls=expected_wait_secs_between_api_calls,
        logger=logging.getLogger(),
    )

    with pytest.raises(TriggerScanException, match=str(expected_error)):
        client.trigger_scan(scan_name="fake_scan", data_timestamp=None)


@responses.activate
def test_trigger_scan_succeed():
    expected_api_base_url = "https://foo.bar"
    expected_trigger_scan_url = urljoin(expected_api_base_url, "api/v1/scans")
    expected_username = "user"
    expected_password = "password"
    expected_wait_secs_between_api_calls = 1
    expected_scan_id = "abc"

    responses.add(
        responses.POST,
        expected_trigger_scan_url,
        status=201,
        headers={"X-Soda-Scan-Id": expected_scan_id},
    )

    client = SodaCloudClient(
        api_base_url=expected_api_base_url,
        username=expected_username,
        password=expected_password,
        wait_secs_between_api_calls=expected_wait_secs_between_api_calls,
        logger=logging.getLogger(),
    )

    client.trigger_scan(scan_name="fake_scan", data_timestamp=None)
    assert responses.calls[0].response.headers["X-Soda-Scan-Id"] == expected_scan_id


@responses.activate
def test_get_status_fails():
    expected_api_base_url = "https://foo.bar"
    scan_id = "abc"
    get_scan_status_endpoint = f"api/v1/scans/{scan_id}"
    expected_get_scan_status_url = urljoin(
        expected_api_base_url, get_scan_status_endpoint
    )
    expected_username = "user"
    expected_password = "password"
    expected_wait_secs_between_api_calls = 1
    expected_error = {"error": "Error!"}

    responses.add(
        responses.GET, expected_get_scan_status_url, status=500, json=expected_error
    )

    client = SodaCloudClient(
        api_base_url=expected_api_base_url,
        username=expected_username,
        password=expected_password,
        wait_secs_between_api_calls=expected_wait_secs_between_api_calls,
        logger=logging.getLogger(),
    )

    with pytest.raises(GetScanStatusException, match=str(expected_error)):
        client.get_scan_status(scan_id=scan_id)


@responses.activate
def test_get_scan_status_succeed():
    expected_api_base_url = "https://foo.bar"
    scan_id = "abc"
    get_scan_status_endpoint = f"api/v1/scans/{scan_id}"
    expected_get_scan_status_url = urljoin(
        expected_api_base_url, get_scan_status_endpoint
    )
    expected_username = "user"
    expected_password = "password"
    expected_wait_secs_between_api_calls = 1
    expected_status = {
        "agentId": "the_agent",
        "checks": [{"evaluationStatus": "pass", "id": "the_check"}],
        "cloudUrl": "the_url",
        "created": "the_creation_time",
        "ended": "the_ended_time",
        "errors": 0,
        "failures": 0,
        "id": scan_id,
        "scanDefinition": {"id": "the_scan_definition_id", "name": "the_scan_name"},
        "scanTime": "the_scan_time",
        "started": "the_start_time",
        "state": "queuing",
        "submitted": "the_submitted_time",
        "warnings": 0,
    }

    responses.add(
        responses.GET, expected_get_scan_status_url, status=200, json=expected_status
    )

    client = SodaCloudClient(
        api_base_url=expected_api_base_url,
        username=expected_username,
        password=expected_password,
        wait_secs_between_api_calls=expected_wait_secs_between_api_calls,
        logger=logging.getLogger(),
    )

    status = client.get_scan_status(scan_id=scan_id)
    assert status == expected_status


@responses.activate
def test_get_scan_logs_fails():
    expected_api_base_url = "https://foo.bar"
    scan_id = "abc"
    get_scan_status_endpoint = f"api/v1/scans/{scan_id}"
    get_scan_logs_endpoint = f"api/v1/scans/{scan_id}/logs"

    expected_get_scan_status_url = urljoin(
        expected_api_base_url, get_scan_status_endpoint
    )
    expected_get_scan_logs_url = urljoin(expected_api_base_url, get_scan_logs_endpoint)

    expected_username = "user"
    expected_password = "password"
    expected_wait_secs_between_api_calls = 1

    expected_error = {"error": "Error!"}
    expected_status = {
        "agentId": "the_agent",
        "checks": [{"evaluationStatus": "pass", "id": "the_check"}],
        "cloudUrl": "the_url",
        "created": "the_creation_time",
        "ended": "the_ended_time",
        "errors": 0,
        "failures": 0,
        "id": scan_id,
        "scanDefinition": {"id": "the_scan_definition_id", "name": "the_scan_name"},
        "scanTime": "the_scan_time",
        "started": "the_start_time",
        "state": "queuing",
        "submitted": "the_submitted_time",
        "warnings": 0,
    }

    responses.add(
        responses.GET, expected_get_scan_status_url, status=200, json=expected_status
    )

    responses.add(
        responses.GET, expected_get_scan_logs_url, status=500, json=expected_error
    )

    client = SodaCloudClient(
        api_base_url=expected_api_base_url,
        username=expected_username,
        password=expected_password,
        wait_secs_between_api_calls=expected_wait_secs_between_api_calls,
        logger=logging.getLogger(),
    )

    with pytest.raises(GetScanLogsException, match=str(expected_error)):
        client.get_scan_logs(scan_id=scan_id)

    assert responses.calls[0].request.url == expected_get_scan_status_url
    assert responses.calls[0].response.status_code == 200
    assert responses.calls[1].request.url == expected_get_scan_logs_url


@responses.activate
def test_get_scan_logs_succeed():
    expected_api_base_url = "https://foo.bar"
    scan_id = "abc"
    get_scan_status_endpoint = f"api/v1/scans/{scan_id}"
    get_scan_logs_endpoint = f"api/v1/scans/{scan_id}/logs"

    expected_get_scan_status_url = urljoin(
        expected_api_base_url, get_scan_status_endpoint
    )
    expected_get_scan_logs_url = urljoin(expected_api_base_url, get_scan_logs_endpoint)

    expected_username = "user"
    expected_password = "password"
    expected_wait_secs_between_api_calls = 1

    expected_status = {
        "agentId": "the_agent",
        "checks": [{"evaluationStatus": "pass", "id": "the_check"}],
        "cloudUrl": "the_url",
        "created": "the_creation_time",
        "ended": "the_ended_time",
        "errors": 0,
        "failures": 0,
        "id": scan_id,
        "scanDefinition": {"id": "the_scan_definition_id", "name": "the_scan_name"},
        "scanTime": "the_scan_time",
        "started": "the_start_time",
        "state": "queuing",
        "submitted": "the_submitted_time",
        "warnings": 0,
    }

    expected_content = {"content": [{"row1": "log1"}, {"row2": "log2"}], "last": True}

    responses.add(
        responses.GET, expected_get_scan_status_url, status=200, json=expected_status
    )

    responses.add(
        responses.GET, expected_get_scan_logs_url, status=200, json=expected_content
    )

    client = SodaCloudClient(
        api_base_url=expected_api_base_url,
        username=expected_username,
        password=expected_password,
        wait_secs_between_api_calls=expected_wait_secs_between_api_calls,
        logger=logging.getLogger(),
    )

    logs = client.get_scan_logs(scan_id=scan_id)

    assert responses.calls[0].request.url == expected_get_scan_status_url
    assert responses.calls[0].response.status_code == 200
    assert responses.calls[1].request.url == expected_get_scan_logs_url
    assert logs == expected_content["content"]


@responses.activate
def test_get_logs_with_waiting_succeed():
    expected_api_base_url = "https://foo.bar"
    scan_id = "abc"
    get_scan_status_endpoint = f"api/v1/scans/{scan_id}"
    get_scan_logs_endpoint = f"api/v1/scans/{scan_id}/logs"

    expected_get_scan_status_url = urljoin(
        expected_api_base_url, get_scan_status_endpoint
    )
    expected_get_scan_logs_url = urljoin(expected_api_base_url, get_scan_logs_endpoint)

    expected_username = "user"
    expected_password = "password"
    expected_wait_secs_between_api_calls = 1

    # First call to get scan status
    first_call_expected_status = {
        "agentId": "the_agent",
        "checks": [{"evaluationStatus": "pass", "id": "the_check"}],
        "cloudUrl": "the_url",
        "created": "the_creation_time",
        "errors": 0,
        "failures": 0,
        "id": scan_id,
        "scanDefinition": {"id": "the_scan_definition_id", "name": "the_scan_name"},
        "scanTime": "the_scan_time",
        "started": "the_start_time",
        "state": "queuing",
        "submitted": "the_submitted_time",
        "warnings": 0,
    }

    responses.add(
        responses.GET,
        expected_get_scan_status_url,
        status=200,
        json=first_call_expected_status,
    )

    # Second call to get expected status
    second_call_expected_status = {
        "agentId": "the_agent",
        "checks": [{"evaluationStatus": "pass", "id": "the_check"}],
        "cloudUrl": "the_url",
        "created": "the_creation_time",
        "errors": 0,
        "failures": 0,
        "id": scan_id,
        "scanDefinition": {"id": "the_scan_definition_id", "name": "the_scan_name"},
        "ended": "the_ended_time",
        "scanTime": "the_scan_time",
        "started": "the_start_time",
        "state": "completed",
        "submitted": "the_submitted_time",
        "warnings": 0,
    }

    responses.add(
        responses.GET,
        expected_get_scan_status_url,
        status=200,
        json=second_call_expected_status,
    )

    # First call to get scan logs
    first_call_expected_logs = {
        "content": [{"row1": "log1"}, {"row2": "log2"}],
        "last": False,
    }

    responses.add(
        responses.GET,
        expected_get_scan_logs_url,
        status=200,
        json=first_call_expected_logs,
    )

    # Second call to get scan logs
    second_call_expected_logs = {
        "content": [{"row3": "log3"}, {"row4": "log4"}],
        "last": True,
    }

    responses.add(
        responses.GET,
        expected_get_scan_logs_url,
        status=200,
        json=second_call_expected_logs,
    )

    client = SodaCloudClient(
        api_base_url=expected_api_base_url,
        username=expected_username,
        password=expected_password,
        wait_secs_between_api_calls=expected_wait_secs_between_api_calls,
        logger=logging.getLogger(),
    )

    logs = client.get_scan_logs(scan_id=scan_id)

    assert responses.calls[0].request.url == expected_get_scan_status_url
    assert responses.calls[0].response.status_code == 200
    assert responses.calls[1].request.url == expected_get_scan_status_url
    assert responses.calls[1].response.status_code == 200
    assert responses.calls[2].request.url == expected_get_scan_logs_url
    assert responses.calls[2].response.status_code == 200
    assert responses.calls[3].request.url == expected_get_scan_logs_url
    assert (
        logs
        == first_call_expected_logs["content"] + second_call_expected_logs["content"]
    )
