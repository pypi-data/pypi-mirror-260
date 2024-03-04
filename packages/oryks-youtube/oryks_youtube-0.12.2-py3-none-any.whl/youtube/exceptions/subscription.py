class SubscriptionDuplicate(Exception):
    """The subscription that you are trying to create already exists."""


class SubscriptionNotFound(Exception):
    """The subscription that you are trying to delete cannot be found."""


class SubscriptionForbidden(Exception):
    """The request is not properly authenticated or not supported for this channel."""
