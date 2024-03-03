"""Errors raised by corvic_check."""

import click


class CommandError(Exception):
    """A check command failed."""

    def __init__(self):
        """Create a command error.

        The sub-command writes error details to the console. So this class
        doesn't need to capture them too.
        """


class CheckError(Exception):
    """A general check error."""

    def __init__(self, message: str):
        """Create a general check error."""
        super().__init__(message)


class MissingToolError(click.ClickException):
    """Raised when check could not find a tool needed to do its job."""
