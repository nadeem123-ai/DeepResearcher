# ============================================================
# utils/retry.py
# Retry decorator — wraps any function with automatic retries.
#
# Usage:
#   from utils.retry import retry
#
#   @retry(attempts=3, delay=2.0)
#   def call_tavily(query):
#       return tavily.invoke(query)
#
# If all attempts fail the last exception is re-raised.
# ============================================================

import time
import functools
from utils.logger import get_logger

log = get_logger(__name__)


def retry(attempts: int = 3, delay: float = 2.0, exceptions: tuple = (Exception,)):
    """
    Decorator factory.

    Args:
        attempts  : max number of tries (default 3)
        delay     : seconds to wait between retries (default 2)
        exceptions: which exception types to catch (default all)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < attempts:
                        log.warning(
                            f"{func.__name__} failed (attempt {attempt}/{attempts}): "
                            f"{exc} — retrying in {delay}s…"
                        )
                        time.sleep(delay)
                    else:
                        log.error(
                            f"{func.__name__} failed after {attempts} attempts: {exc}"
                        )
            if last_exc is not None:
                raise last_exc
        return wrapper
    return decorator