class AioDeepLException(Exception):
    """Base exception for all exceptions raised by the library."""

class TooManyRequests(AioDeepLException):
    """Raised when the user has sent too many requests in a given amount of time."""

class QuotaExceeded(AioDeepLException):
    """Raised when the user has exceeded their quota."""

class BackendError(AioDeepLException):
    """Raised when the DeepL server returns an error."""
