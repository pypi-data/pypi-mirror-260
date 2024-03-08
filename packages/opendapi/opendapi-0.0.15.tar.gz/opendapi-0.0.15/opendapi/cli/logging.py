"""Debugging utilities for OpenDAPI"""

from importlib.metadata import version
from urllib.parse import urljoin

import requests
import sentry_sdk

DAPI_API_KEY_HEADER = "X-DAPI-Server-API-Key"
WOVEN_DENY_LIST = sentry_sdk.scrubber.DEFAULT_DENYLIST + [DAPI_API_KEY_HEADER]


def sentry_init(dapi_server_host: str = None, dapi_server_api_key: str = None):
    """Initialize sentry, but silently fail in case of errors"""

    # Silently return if we don't have the required information
    if not dapi_server_host or not dapi_server_api_key:
        return

    try:
        response = requests.get(
            urljoin(dapi_server_host, "/v1/config/client/opendapi"),
            headers={
                "Content-Type": "application/json",
                DAPI_API_KEY_HEADER: dapi_server_api_key,
            },
            timeout=60,
        )

        # We will silently ignore any errors
        response.raise_for_status()

        # Try and initialize sentry so we can capture all the errors
        config = response.json()
        sentry_config = config.get("sentry", {})

        if sentry_config:
            sentry_config["release"] = version("opendapi")
            sentry_config["event_scrubber"] = sentry_sdk.scrubber.EventScrubber(
                denylist=WOVEN_DENY_LIST
            )
            sentry_sdk.init(**config["sentry"])

        # Set sentry tags
        sentry_tags = config.get("sentry_tags", {})
        if sentry_config and sentry_tags:
            for tag, value in sentry_tags.items():
                sentry_sdk.set_tag(tag, value)

    except Exception:  # pylint: disable=broad-except
        pass  # nosec B110
