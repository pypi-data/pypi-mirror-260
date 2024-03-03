"""Errors specific to communicating with the database."""

from corvic import result


class AuthenticationError(result.Error):
    """Could not determine which user to use for database auth."""


class InvalidORMIdentifierError(result.Error):
    """Raised when an identifier can't be translated to its orm equivalent."""


class RequestedObjectsForNobodyError(result.Error):
    """Raised when attempts are made to access database objects as the nobody org."""
