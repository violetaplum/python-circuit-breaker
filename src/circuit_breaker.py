from enum import Enum
from datetime import datetime, timedelta
from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self._can_execute():
                try:
                    result = func(*args, **kwargs)
                    self._handle_success()
                    return result
                except Exception as e:
                    self._handle_failure()
                    raise e
            else:
                raise Exception("Circuit breaker is OPEN")
        return wrapper

    def _can_execute(self):
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            if self.last_failure_time and datetime.now() - self.last_failure_time > timedelta(seconds=self.reset_timeout):
                self.state = CircuitState.HALF_OPEN
                return True
        return False

    def _handle_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        logger.info(f"Circuit breaker state: {self.state}")

    def _handle_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker state changed to: {self.state}")

