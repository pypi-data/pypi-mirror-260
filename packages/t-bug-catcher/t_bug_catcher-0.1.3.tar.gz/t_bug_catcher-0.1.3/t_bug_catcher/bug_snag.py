import sys
from typing import Optional

import bugsnag

from .utils import logger
from .workitems import variables


class BugSnag:
    """BugSnag class for interacting with the BugSnag API."""

    def __init__(self):
        """Initializes the BugSnag class."""
        pass

    def config(self, api_key: str):
        """Configures the BugSnag class.

        Args:
            api_key (str): The API key for the BugSnag account.

        Returns:
            None
        """
        self._api_key = api_key
        bugsnag.configure(api_key=api_key, release_stage=variables.get("environment", "Local"))
        bugsnag.add_metadata_tab(
            "Metadata",
            {
                "run_url": variables.get("processRunUrl", ""),
                "run_by": variables.get("userEmail", ""),
            },
        )

    def report_error(self, exception: Optional[Exception] = None, metadata: Optional[dict] = None):
        """Sends an error to BugSnag.

        Args:
            exception (Exception, optional): The exception to report.
            metadata (dict, optional): The metadata to be added to the Bugsnag issue. Defaults to None.

        Returns:
            None
        """
        if not exception:
            _, exception, _ = sys.exc_info()
        if isinstance(metadata, dict):
            bugsnag.notify(exception=exception, metadata={"special_info": metadata})
            return
        if metadata is None:
            bugsnag.notify(exception=exception)
            return
        logger.warning(f"Incorrect type of metadata: {type(metadata)}")
        bugsnag.notify(exception=exception)
