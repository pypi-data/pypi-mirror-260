class DoesNotExist(Exception):
    """Raise when entity not found in database."""


class AlreadyExists(Exception):
    """Raise when entity already exists."""


class Unauthorized(Exception):
    """Raise when authentication fails."""
