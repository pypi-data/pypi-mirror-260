"""
Collection of tasks to interact with Soda Cloud
"""

from datetime import datetime
from typing import List, Optional

from prefect import get_run_logger, task

from prefect_soda_cloud import SodaCloudAuthConfig


@task
def trigger_scan(
    scan_name: str,
    soda_cloud_auth_config: SodaCloudAuthConfig,
    data_timestamp: Optional[datetime] = None,
) -> str:
    """
    Trigger a scan given its name.

    Args:
        scan_name: The name of the scan to trigger.
        soda_cloud_auth_config: The auth configuration to use to trigger the scan.

    Returns:
        The Scan identifier.

    Example:
    ```python
    from prefect_soda_cloud import SodaCloudAuthConfig, SodaCloudCredentials
    from prefect_soda_cloud.tasks import trigger_scan

    creds = SodaCloudCredentials(
        user_or_api_key_id="the_user",
        pwd_or_api_key_secret="the_password"
    )

    auth_config = SodaCloudAuthConfig(
        api_base_url="https://cloud.soda.io",
        creds=creds
    )

    scan_id = trigger_scan(
        soda_cloud_auth_config=auth_config,
        data_timestamp=None
    )
    ```
    """
    soda_cloud_client = soda_cloud_auth_config.get_client(logger=get_run_logger())
    scan_id = soda_cloud_client.trigger_scan(
        scan_name=scan_name, data_timestamp=data_timestamp
    )

    return scan_id


@task
def get_scan_status(
    scan_id: str,
    soda_cloud_auth_config: SodaCloudAuthConfig,
    wait_for_scan_end: bool = False,
) -> dict:
    """
    Retrieve scan status from Soda Cloud given the scan ID.

    Args:
        scan_id: Scan identifier provided by Soda Cloud.
        soda_cloud_auth_config: The auth configuration to use to trigger the scan.
        wait_for_scan_end: Whether to wait for the scan execution to finish or not.

    Returns:
        A dictionary that describes the status of the scan.
    """
    soda_cloud_client = soda_cloud_auth_config.get_client(logger=get_run_logger())
    scan_status = soda_cloud_client.get_scan_status(
        scan_id=scan_id, wait_for_scan_end=wait_for_scan_end
    )
    return scan_status


@task
def get_scan_logs(
    scan_id: str, soda_cloud_auth_config: SodaCloudAuthConfig
) -> List[dict]:
    """
    Retrieve scan logs from Soda Cloud given the scan ID.

    Args:
        scan_id: Scan identifier provided by Soda Cloud.
        soda_cloud_auth_config: The auth configuration to use to trigger the scan.

    Returns:
        A list of dict, each dict being a Soda Cloud log message.
    """
    soda_cloud_client = soda_cloud_auth_config.get_client(logger=get_run_logger())
    scan_logs = soda_cloud_client.get_scan_logs(scan_id=scan_id)
    return scan_logs
