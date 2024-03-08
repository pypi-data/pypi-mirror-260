"""
Exceptions to handle failures during interactions with Soda Cloud APIs.
"""


class TriggerScanException(Exception):
    """
    Exception to raise when there's an issue with Soda Cloud Trigger Scan API.
    """


class GetScanStatusException(Exception):
    """
    Exception to raise when there's an issue with Soda Cloud Get Scan Status API.
    """


class GetScanLogsException(Exception):
    """
    Exception to raise when there's an issue with Soda Cloud Get Scan Logs API.
    """
