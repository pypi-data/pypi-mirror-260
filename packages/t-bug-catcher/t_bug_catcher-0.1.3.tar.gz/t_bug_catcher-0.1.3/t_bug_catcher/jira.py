"""JiraPoster class for interacting with the Jira API."""

import datetime
import hashlib
import json
import os
import re
import sys
import traceback
from pathlib import Path
from typing import List, Optional

import requests
from requests.auth import HTTPBasicAuth
from retry import retry

from .config import CONFIG
from .exceptions import BadRequestError
from .utils import logger
from .workitems import variables


def retry_if_bad_request(func):
    """Retries a function if it raises a BadRequestError."""
    attempt = 1
    tries = 3

    @retry(exceptions=BadRequestError, tries=tries, delay=1, backoff=2)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadRequestError as ex:
            nonlocal attempt
            print(f"Bad request Attempt {attempt}...", "WARN")
            attempt = attempt + 1 if attempt < tries else 1
            raise ex

    return wrapper


class Jira:
    """Jira class for interacting with the Jira API."""

    def __init__(self):
        """Initializes the Jira class."""
        self._base_url = "https://thoughtfulautomation.atlassian.net/"
        self._assignee_cache = {}
        self._transition_types = {}
        self._issue_types = {}
        self._project_key = None
        self._webhook_url = None
        self._auth = None

    @staticmethod
    def _is_json_response(response) -> bool:
        try:
            response.json()
            return True
        except json.decoder.JSONDecodeError:
            return False

    def check_response(self, response, mandatory_json: bool = False, exc_message: str = "") -> None:
        """Check if response is not 200 or not json.

        Args:
            response (requests.Response): The response object
            mandatory_json (bool, optional): If the response is not json. Defaults to False.
            exc_message (str, optional): The exception message. Defaults to "".

        Raises:
            BadRequestError: If the response is not 200 or not json

        Returns:
            None
        """
        # Check if response is not 200 or not json
        if response.status_code not in [200, 201] or (mandatory_json and not self._is_json_response(response)):
            exc_message = exc_message + "\n" if exc_message else ""
            if self._is_json_response(response):
                raise BadRequestError(
                    f"{exc_message}Status Code: {response.status_code}, "
                    f"Json content: {response.json()}, Headers: {response.headers}"
                )
            else:
                raise BadRequestError(
                    f"{exc_message}Status Code: {response.status_code}, " f"Headers: {response.headers}"
                )

    def config(self, login, api_token, project_key, webhook_url: Optional[str]):
        """Sets the webhook URL for the Jira project.

        Args:
            login (str): The username for the Jira account.
            api_token (str): The API token for the Jira account.
            project_key (str): The key of the Jira project.
            webhook_url (str): The webhook URL for the Jira project.

        Returns:
            None
        """
        self._project_key = project_key
        if not webhook_url:
            logger.warning("No JIRA webhook URL provided. All issues will be posted to backlog.")
        self._webhook_url = webhook_url
        self._auth = self._authenticate(login, api_token)
        try:
            self._issue_types = self.__get_issue_types()
        except BadRequestError:
            self._auth = None
            logger.warning("Failed to authenticate or incorrect project key.")

    def _authenticate(self, login, api_token) -> HTTPBasicAuth:
        """Function to authenticate the user with the provided username and API token.

        Returns:
            HTTPBasicAuth: The authentication object for the Jira API.
        """
        return HTTPBasicAuth(login, api_token)

    def __get_headers(self) -> dict:
        """A function to get the headers for a Jira API request.

        Returns:
            dict: The headers for the Jira API request.
        """
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @retry_if_bad_request
    def get_issues(self) -> dict:
        """A function to get the issues using a Jira API.

        It updates the headers, sets up a JQL query, specifies additional query parameters,
        makes a GET request to the Jira API, and returns the JSON response.
        """
        jql_query = f'project = "{self._project_key}"'

        # Specify additional query parameters if needed
        query_params = {"jql": jql_query, "maxResults": 100}  # Adjust as needed

        response = requests.request(
            "GET",
            self._base_url + "/rest/api/2/search",
            headers=self.__get_headers(),
            auth=self._auth,
            params=query_params,
        )
        self.check_response(response)
        return response.json()

    @retry_if_bad_request
    def get_issue(self, issue_id: str):
        """A function to get the issue using a Jira API.

        Args:
            issue_id (str): The ID of the issue.

        Returns:
            dict: The JSON response from the Jira API.
        """
        response = requests.request(
            "GET",
            url=self._base_url + f"/rest/api/3/issue/{issue_id}",
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return response.json()

    def __generate_issue_body(self, summary: str, description: dict, assignee: str, issue_type: str) -> str:
        """Generates the issue body payload for creating a new issue.

        Args:
            summary (str): The summary of the issue.
            description (dict): The description of the issue.
            assignee (str): The assignee of the issue.
            issue_type (str): The type of the issue.

        Returns:
            The JSON payload for creating a new issue.
        """
        payload = json.dumps(
            {
                "fields": {
                    "assignee": {"id": assignee if assignee else "-1"},
                    "description": description,
                    "issuetype": {"id": issue_type},
                    "project": {"key": self._project_key},
                    "summary": summary,
                },
            }
        )
        return payload

    def move_ticket_to_board(self, ticket_id: str) -> None:
        """Move a ticket to a board using its ID.

        Args:
            self: The object instance
            ticket_id (str): The ID of the ticket to be moved

        Returns:
            None
        """
        payload = json.dumps({"issues": [ticket_id]})
        requests.request(
            "POST",
            url=self._webhook_url,
            headers={"Content-type": "application/json"},
            data=payload,
        )

    def __get_issue_types(self) -> dict:
        """Get the board information.

        Args:
            self: The object instance

        Returns:
            dict: The board information
        """
        response = requests.request(
            "GET",
            url=self._base_url + f"/rest/api/3/project/{self._project_key}",
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return {issue_type["name"].lower(): issue_type["id"] for issue_type in response.json()["issueTypes"]}

    @retry_if_bad_request
    def __get_transtion_types(self, issue_id: str) -> dict:
        """Get the board information.

        Args:
            self: The object instance
            issue_id (str): The ID of the issue

        Returns:
            dict: The board information
        """
        if self._transition_types.get("to do"):
            return self._transition_types

        response = requests.request(
            "GET",
            url=self._base_url + f"/rest/api/3/issue/{issue_id}/transitions",
            headers=self.__get_headers(),
            auth=self._auth,
        )

        self.check_response(response)
        return {
            transition_type["name"].lower(): transition_type["id"] for transition_type in response.json()["transitions"]
        }

    def __create_description_markup(
        self,
        error_string: str,
        exception: Exception,
        error_id: str,
        additional_info: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Create a description with the given trace_back and additional_info.

        Args:
            error_string (str): The error string.
            exception (Exception): The exception object.
            error_id (str): The error ID.
            additional_info (str, optional): Additional information. Defaults to "".
            metadata (dict, optional): Additional metadata. Defaults to None.

        Returns:
            dict: A dictionary containing the version, type, and content.
        """
        try:
            exc_traceback = "".join(traceback.format_exception(exception))
        except TypeError:
            exc_traceback = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        additional_info_markup = [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Additional info: ",
                        "marks": [{"type": "strong"}],
                    },
                    {
                        "type": "text",
                        "text": additional_info,
                    },
                ],
            }
        ]

        exc_info = f"{exception.__class__.__name__}: {str(exception)}"

        error_string_markup = [
            {
                "type": "panel",
                "attrs": {"panelType": "error"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": error_string,
                                "marks": [{"type": "code"}],
                            },
                        ],
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    exc_info
                                    if len(exc_info) < CONFIG.LIMITS.MAX_DESCRIPTION_LENGTH
                                    else exc_info[: CONFIG.LIMITS.MAX_DESCRIPTION_LENGTH] + "..."
                                ),
                            }
                        ],
                    },
                ],
            }
        ]

        date_markup = [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Error time: ",
                        "marks": [{"type": "strong"}],
                    },
                    {
                        "type": "text",
                        "text": str(datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")),
                    },
                ],
            }
        ]

        runlink_markup = [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Run link: ",
                        "marks": [{"type": "strong"}],
                    },
                    {
                        "type": "text",
                        "text": (" " if variables.get("processRunUrl") is None else variables.get("processRunUrl")),
                        "marks": (
                            [] + [{"type": "strong"}]
                            if variables.get("processRunUrl") is None
                            else [
                                {
                                    "type": "link",
                                    "attrs": {"href": variables.get("processRunUrl")},
                                }
                            ]
                        ),
                    },
                ],
            }
        ]

        environment_markup = [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Environment: ",
                        "marks": [{"type": "strong"}],
                    },
                    {
                        "type": "text",
                        "text": ("Local" if variables.get("environment") is None else variables.get("environment")),
                    },
                ],
            }
        ]

        traceback_markup = [
            {
                "type": "expand",
                "attrs": {"title": "Traceback"},
                "content": [
                    {
                        "type": "codeBlock",
                        "attrs": {},
                        "content": [
                            {
                                "type": "text",
                                "text": exc_traceback,
                            }
                        ],
                    },
                ],
            }
        ]

        error_id_markup = [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"Error string ID: {error_id}",
                        "marks": [
                            {"type": "em"},
                            {"type": "subsup", "attrs": {"type": "sub"}},
                        ],
                    },
                ],
            },
        ]

        metadata_markup = [
            {
                "type": "expand",
                "attrs": {"title": "Metadata"},
                "content": [
                    {
                        "type": "codeBlock",
                        "attrs": {"language": "json"},
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(metadata, indent=4),
                            }
                        ],
                    },
                ],
            }
        ]

        return {
            "version": 1,
            "type": "doc",
            "content": []
            + (error_string_markup if error_string else [])
            + date_markup
            + (runlink_markup if variables.get("processRunUrl") else [])
            + environment_markup
            + (additional_info_markup if additional_info else [])
            + traceback_markup
            + (metadata_markup if metadata else [])
            + error_id_markup,
        }

    def __create_transtion_markup(self, issue_status: str) -> dict:
        """Create a transition markup.

        Args:
            issue_status (str): The status of the Jira issue.

        Returns:
            dict: The transition markup.
        """
        {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Status of ticket have been changed by Bot: ",
                            },
                            {
                                "type": "text",
                                "text": issue_status,
                                "marks": [{"type": "strong"}],
                            },
                            {
                                "type": "text",
                                "text": " -> ",
                            },
                            {
                                "type": "text",
                                "text": "To Do",
                                "marks": [{"type": "strong"}],
                            },
                        ],
                    },
                ],
            }
        }

    def __create_comment_markup(
        self,
        error: Optional[str] = None,
        attachments: Optional[List] = None,
        additional_info: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Create a comment with the given error and attachments.

        Args:
            error (str): The error string.
            attachments (List): The list of attachments.
            issue_status (str, optional): The issue status. Defaults to "".
            additional_info (str, optional): Additional information. Defaults to "".

        Returns:
            dict: The comment.

        """
        if error:
            error = (
                error
                if len(error) < CONFIG.LIMITS.MAX_DESCRIPTION_LENGTH
                else error[: CONFIG.LIMITS.MAX_DESCRIPTION_LENGTH] + "..."
            )
        error_markup = [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Error occures again in "},
                    {
                        "type": "text",
                        "text": (
                            "local run" if variables.get("processRunUrl") is None else variables.get("processRunUrl")
                        ),
                        "marks": (
                            [] + [{"type": "underline"}]
                            if variables.get("processRunUrl") is None
                            else [
                                {
                                    "type": "link",
                                    "attrs": {"href": variables.get("processRunUrl")},
                                },
                                {"type": "underline"},
                            ]
                        ),
                    },
                    {
                        "type": "text",
                        "text": f" at {str(datetime.datetime.now().strftime('%B %d, %Y %I:%M:%S %p'))}",
                    },
                    {"type": "hardBreak"},
                    {
                        "type": "text",
                        "text": error,
                        "marks": [{"type": "code"}],
                    },
                ],
            }
        ]

        attach_markup = [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Attachments: ",
                        "marks": [{"type": "strong"}],
                    },
                ],
            }
        ]
        if attachments:
            for attach in attachments:
                attach_markup[0]["content"].append(
                    {
                        "type": "text",
                        "text": attach[0]["filename"],
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {"href": attach[0]["content"]},
                            }
                        ],
                    },
                )
                attach_markup[0]["content"].append({"type": "text", "text": "; "})

        additional_info_markup = [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"Additional information: {additional_info}",
                    },
                ],
            },
        ]

        metadata_markup = [
            {
                "type": "expand",
                "attrs": {"title": "Metadata"},
                "content": [
                    {
                        "type": "codeBlock",
                        "attrs": {"language": "json"},
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(metadata, indent=4),
                            }
                        ],
                    },
                ],
            }
        ]

        return {
            "body": {
                "type": "doc",
                "version": 1,
                "content": []
                + (error_markup if error else [])
                + (additional_info_markup if additional_info else [])
                + (attach_markup if attachments else [])
                + (metadata_markup if metadata else []),
            }
        }

    @retry_if_bad_request
    def check_issue_status(self, issue_id: str) -> str:
        """Check the status of a Jira issue.

        Args:
            issue_id (str): The ID of the Jira issue.

        Returns:
            The response from checking the status of the Jira issue.
        """
        response = requests.request(
            "GET",
            self._base_url + f"/rest/api/3/issue/{issue_id}",
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return response.json()["fields"]["status"]["name"]

    def report_error(
        self,
        exception: Optional[Exception] = None,
        assignee: Optional[str] = None,
        attachments: Optional[List] = None,
        metadata: Optional[dict] = None,
        additional_info: Optional[str] = None,
    ) -> dict:
        """Create a Jira issue with the given attachments.

        Args:
            exception (Exception, optional): The exception to be added to the Jira issue.
            assignee (str, optional): The assignee to be added to the Jira issue.
            attachments (List, optional): List of attachments to be added to the Jira issue.
            metadata (dict, optional): Metadata to be added to the Jira issue.
            additional_info (str, optional): Additional information to be added to the Jira issue.

        Returns:
            The response from creating the Jira issue.
        """
        if not self._auth:
            logger.warning("Jira auth not provided. Skipping Jira issue creation.")
            return False
        try:
            if not exception:
                _, exception, _ = sys.exc_info()

            if attachments is None:
                attachments = []

            if not isinstance(attachments, List):
                logger.warning(f"Incorrect type of attachments: {type(attachments)}")
                attachments = []

            if hasattr(exception, "custom_attachments"):
                attachments += exception.custom_attachments

            if len(attachments) > CONFIG.LIMITS.MAX_ATTACHMENTS:
                logger.warning(f"Only the first {CONFIG.LIMITS.MAX_ATTACHMENTS} attachments were uploaded.")
            attachments = attachments[: CONFIG.LIMITS.MAX_ATTACHMENTS]

            frames = [
                frame
                for frame in traceback.extract_tb(exception.__traceback__)
                if "site-packages" not in str(frame.filename).lower()
            ]
            file_name, line_no, _, error_string = frames[-1]
            summary = (
                f"[{exception.__class__.__name__}:{os.path.basename(file_name)}:{line_no}] "
                f"{self.remove_locators_from_exception(exception)}"
            )
            error_id = self.__generate_error_id(exception=exception)

            existing_ticket = self.filter_tickets(
                all_tickets=self.get_issues()["issues"],
                error_id=error_id,
            )
            if existing_ticket:
                issue_status = self.check_issue_status(existing_ticket["id"])
                self._transition_types = self.__get_transtion_types(issue_id=existing_ticket["id"])
                if issue_status.lower() != "to do":
                    self.issue_transition(
                        ticket_id=existing_ticket["id"],
                        transition_id=self._transition_types["to do"],
                    )
                    self.update_comment(
                        ticket_id=existing_ticket["id"],
                        comments=self.__create_transtion_markup(
                            issue_status=issue_status,
                        ),
                    )

                issue = self.get_issue(existing_ticket["id"])

                if len(issue["fields"].get("attachment", [])) >= CONFIG.LIMITS.MAX_ISSUE_ATTACHMENTS:
                    logger.warning(
                        f"Attachments were not uploaded due to exceeding "
                        f"{CONFIG.LIMITS.MAX_ISSUE_ATTACHMENTS} attachments limit."
                    )
                    posted_attachments = []
                else:
                    posted_attachments = (
                        [self.add_attachment(attachment, issue["id"]) for attachment in attachments]
                        if attachments
                        else []
                    )

                self.update_comment(
                    ticket_id=issue["id"],
                    comments=self.__create_comment_markup(
                        error=summary,
                        attachments=posted_attachments,
                        additional_info=additional_info,
                        metadata=metadata,
                    ),
                )
                logger.info("Jira issue updated successfully.")
                return True, existing_ticket

            assignee_id = None
            if assignee:
                try:
                    assignee_id = self.__get_assignee(assignee)
                except Exception as ex:
                    logger.info(f"Failed to get assignee {assignee} due to: {ex}")

            description = self.__create_description_markup(
                exception=exception,
                error_string=error_string,
                error_id=error_id,
                additional_info=additional_info,
                metadata=metadata,
            )

            issue = self.__generate_issue_body(
                summary=summary[:255].split("\n")[0],
                description=description,
                assignee=assignee_id,
                issue_type=self._issue_types["bug"],
            )
            response = self.create_ticket(issue=issue)

            if response.status_code != 201:
                logger.warning(
                    f"Failed to create Jira issue. Status code: {response.status_code}"
                    f" Error messages: {', '.join(response.json()['errorMessages'])}"
                    f" Errors: {response.json()['errors']}"
                )
                return False, response

            ticket = response.json()
            ticket_id = ticket["id"]
            if attachments:
                for attachment in attachments:
                    self.add_attachment(attachment, ticket_id)
            if self._webhook_url:
                self.move_ticket_to_board(ticket_id)
            logger.info("Jira issue created successfully.")
            return True, response
        except Exception as ex:
            logger.warning(f"Failed to create Jira issue due to: {ex}")
            return False

    @retry_if_bad_request
    def add_attachment(self, attachment: str, ticket_id: str) -> dict:
        """Uploads an attachment to a Jira ticket.

        Args:
            attachment (str): The path to the file to be attached.
            ticket_id (str): The ID of the Jira ticket.

        Returns:
            None
        """
        if not attachment:
            logger.warning(f"Attachment {attachment} does not exist.")
            return
        if not os.path.exists(attachment):
            logger.warning(f"Attachment {attachment} does not exist.")
            return
        files = {"file": (os.path.basename(attachment), open(attachment, "rb"))}
        headers = {"Accept": "application/json", "X-Atlassian-Token": "no-check"}
        response = requests.request(
            "POST",
            self._base_url + f"/rest/api/3/issue/{ticket_id}/attachments",
            headers=headers,
            auth=self._auth,
            files=files,
        )
        self.check_response(response)
        return response.json()

    @retry_if_bad_request
    def issue_transition(self, ticket_id: str, transition_id: str) -> None:
        """Perform a transition on the given ticket using the provided transition ID.

        Args:
            ticket_id (str): The ID of the ticket to transition.
            transition_id (int): The ID of the transition to be performed.

        Returns:
            None
        """
        payload = json.dumps(
            {
                "transition": {"id": transition_id},
            }
        )
        response = requests.request(
            "POST",
            self._base_url + f"/rest/api/3/issue/{ticket_id}/transitions",
            headers=self.__get_headers(),
            auth=self._auth,
            data=payload,
        )
        self.check_response(response)

    @retry_if_bad_request
    def update_comment(self, ticket_id: str, comments: str) -> None:
        """Updates the comments for a specific ticket.

        Args:
            ticket_id (str): The ID of the ticket.
            comments (str): The comments to be added to the ticket.

        Returns:
            None
        """
        payload = json.dumps(comments)

        response = requests.request(
            "POST",
            self._base_url + f"/rest/api/3/issue/{ticket_id}/comment",
            headers=self.__get_headers(),
            auth=self._auth,
            data=payload,
        )
        self.check_response(response)

    @retry_if_bad_request
    def get_jira_user(self, email: str) -> dict:
        """Get Jira user by email.

        Args:
            email (str): The email of the user.

        Returns:
            The Jira user object.
        """
        response = requests.request(
            "GET",
            self._base_url + f"/rest/api/3/user/search?query={email}",
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return response.json()

    def create_ticket(self, issue: dict) -> requests.Response:
        """Create a ticket using the provided issue data and return the response.

        Args:
            issue (dict): The data for creating the ticket.

        Returns:
            requests.Response: The response object from the ticket creation request.
        """
        response = requests.request(
            "POST",
            self._base_url + "/rest/api/3/issue",
            data=issue,
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return response

    def filter_tickets(self, all_tickets: List, error_id: str) -> dict:
        """Filters tickets based on summary and error string ID and returns a matching ticket if found.

        Args:
            all_tickets (list): List of all tickets to filter.
            error_id (str): The error string ID to filter by.

        Returns:
            dict or None: The matching ticket if found, otherwise None.
        """
        for ticket in all_tickets:
            if not ticket["fields"]["description"]:
                continue
            if error_id not in ticket["fields"]["description"]:
                continue
            return ticket

        else:
            return None

    @staticmethod
    def __generate_error_id(exception: Exception) -> str:
        """Generates an error string ID using the exception, function name, and error string.

        Args:
            exception: The exception object.

        Returns:
            str: The generated error string ID.

        """
        frames = [
            frame
            for frame in traceback.extract_tb(exception.__traceback__)
            if "site-packages" not in str(frame.filename).lower()
        ]
        exception_chain = "-".join([f"{frame.name}" for frame in frames])
        rel_path = os.path.relpath(frames[-1].filename, os.getcwd())
        path = Path(os.path.splitext(rel_path)[0]).as_posix()
        error_id = (
            f"{path}-{exception_chain}-{frames[-1].line}-"
            f"{exception.__class__.__module__}-{exception.__class__.__name__}"
        )
        return hashlib.md5(error_id.encode()).hexdigest()

    def __get_assignee(self, assignee: str) -> str:
        """Get assignee Jira user by ID.

        Args:
            assignee (str): The ID of the assignee.

        Returns:
            str: The ID of the assignee.
        """
        if assignee in self._assignee_cache:
            return self._assignee_cache[assignee]
        response = self.get_jira_user(assignee)
        self._assignee_cache[assignee] = response[0]["accountId"]
        return response[0]["accountId"]

    def remove_locators_from_exception(self, exception: Exception) -> str:
        """Remove locators from the exception.

        Args:
            exception: The exception object.

        Returns:
            str: The cleaned exception string.
        """
        if "selenium" not in exception.__class__.__name__.lower() and not isinstance(exception, AssertionError):
            return str(exception)
        return re.sub(r"\'(.+)\'", "'...'", str(exception))
