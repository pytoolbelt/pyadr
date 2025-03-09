import functools
from pyadr import config

from .exceptions import PyadrError


class ErrorHandler:
    def __init__(self) -> None:
        self.debug = config.PYADR_DEBUG

    def handle(self, exception: Exception) -> int:
        return self.reraise_if_debug(exception)

    def reraise_if_debug(self, exception: Exception) -> int:
        """Reraise exception if we are debugging."""
        if self.debug:
            raise exception
        else:
            return 1


def handle_cli_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        error_handler = ErrorHandler()

        try:
            return func(*args, **kwargs)

        except PermissionError as e:
            return error_handler.handle(e)

        except FileNotFoundError as e:
            return error_handler.handle(e)

        except OSError as e:
            return error_handler.handle(e)

        except PyadrError as e:
            return error_handler.handle(e)

    return wrapper
