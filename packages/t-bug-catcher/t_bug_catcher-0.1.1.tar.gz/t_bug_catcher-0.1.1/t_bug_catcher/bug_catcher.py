"""JiraPoster class for interacting with the Jira API."""
from typing import List, Optional

from .bug_snag import BugSnag
from .jira import Jira


class Configurator:
    """Configurer class for configuring the JiraPoster and BugSnag."""

    def __init__(self, jira, bugsnag):
        """Initializes the Configurer class."""
        self.__jira = jira
        self.__bug_snag = bugsnag

    def jira(
        self,
        login: str,
        api_token: str,
        project_key: str,
        webhook_url: Optional[str] = None,
    ):
        """Configures the JiraPoster and BugSnag classes.

        Args:
            login (str): The username for the Jira account.
            api_token (str): The API token for the Jira account.
            project_key (str): The key of the Jira project.
            webhook_url (str, optional): The webhook URL for the Jira project. Defaults to None.

        Returns:
            None
        """
        self.__jira.config(
            login=login,
            api_token=api_token,
            project_key=project_key,
            webhook_url=webhook_url,
        )

    def bugsnag(self, api_token: str):
        """Configures the BugSnag class.

        Args:
            api_token (str): The API token for the BugSnag account.

        Returns:
            None
        """
        self.__bug_snag.config(api_key=api_token)


class BugCatcher:
    """BugCatcher class for interacting with the Jira API."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one BugCatcher instance is created."""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initializes the BugCatcher class."""
        self.__jira = Jira()
        self.__bug_snag = BugSnag()
        self.__configurator = Configurator(self.__jira, self.__bug_snag)

    @property
    def configure(self):
        """Configures the JiraPoster and BugSnag classes."""
        return self.__configurator

    def report_error(
        self,
        exception: Optional[Exception] = None,
        description: Optional[str] = "",
        metadata: Optional[dict] = None,
        attachments: Optional[List] = None,
        assignee: Optional[str] = None,
    ):
        """Reports an error to the Jira project.

        Args:
            exception (Exception, optional): The exception to report. Defaults to None.
            description (str, optional): The description of the error. Defaults to "".
            metadata (dict, optional): The metadata to be added to the Jira issue. Defaults to None.
            attachments (List, optional): The attachments to be added to the Jira issue. Defaults to None.
            assignee (str, optional): The assignee to be added to the Jira issue. Defaults to None.

        Returns:
            None
        """
        self.__jira.report_error(
            exception=exception,
            assignee=assignee,
            attachments=attachments,
            additional_info=description,
            metadata=metadata,
        )

        self.__bug_snag.report_error(
            exception=exception,
            metadata=metadata,
        )

    def report_error_to_jira(
        self,
        exception: Optional[Exception] = None,
        assignee: Optional[str] = None,
        attachments: Optional[List] = None,
        metadata: Optional[dict] = None,
        additional_info: Optional[str] = None,
    ):
        """Creates a Jira issue with the given attachments.

        Args:
            exception (Exception, optional): The exception to report. Defaults to None.
            assignee (str, optional): The assignee to be added to the Jira issue. Defaults to None.
            attachments (List, optional): The attachments to be added to the Jira issue. Defaults to None.
            additional_info (str, optional): The additional information to be added to the Jira issue. Defaults to "".
            metadata (dict, optional): The metadata to be added to the Jira issue. Defaults to None.

        Returns:
            None

        """
        self.__jira.report_error(
            exception=exception,
            assignee=assignee,
            attachments=attachments,
            additional_info=additional_info,
            metadata=metadata,
        )

    def report_error_to_bugsnag(self, exception: Optional[Exception] = None, metadata: Optional[dict] = None):
        """Sends an error to BugSnag.

        Args:
            exception (Exception): The exception to report.
            metadata (dict, optional): The metadata to be added to the Bugsnag issue. Defaults to None.

        Returns:
            None

        """
        self.__bug_snag.report_error(
            exception=exception,
            metadata=metadata,
        )

    @staticmethod
    def attach_file_to_exception(exception: Exception, attachment: str) -> None:
        """Update the exception with the given attachment.

        Args:
            exception (Exception): The exception to update.
            attachment (str): The attachment to add to the exception.

        Returns:
            None
        """
        if hasattr(exception, "custom_attachments"):
            exception.custom_attachments.append(attachment)
        else:
            exception.custom_attachments = [attachment]


__bug_catcher = BugCatcher()

configure = __bug_catcher.configure
report_error = __bug_catcher.report_error
attach_file_to_exception = __bug_catcher.attach_file_to_exception
report_error_to_jira = __bug_catcher.report_error_to_jira
report_error_to_bugsnag = __bug_catcher.report_error_to_bugsnag
