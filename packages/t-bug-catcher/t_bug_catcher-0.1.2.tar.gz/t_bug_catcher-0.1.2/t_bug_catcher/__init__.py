"""Top-level package for t-bug-catcher."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
__version__ = '0.1.2'  # fmt: skip

from .bug_catcher import (
    configure,
    report_error,
    report_error_to_jira,
    report_error_to_bugsnag,
    attach_file_to_exception,
)

__all__ = [
    "configure",
    "report_error",
    "report_error_to_jira",
    "report_error_to_bugsnag",
    "attach_file_to_exception",
]
