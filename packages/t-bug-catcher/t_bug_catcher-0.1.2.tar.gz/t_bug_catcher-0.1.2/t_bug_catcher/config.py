class Config:
    """Config class for configuring the application."""

    class LIMITS:
        """Limits class for configuring the application."""

        MAX_ATTACHMENTS: int = 5
        MAX_ISSUE_ATTACHMENTS: int = 100
        MAX_DESCRIPTION_LENGTH: int = 250


CONFIG = Config()
