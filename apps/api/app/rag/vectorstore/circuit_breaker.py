import time


class CircuitBreaker:
    """
    A simple circuit breaker implementation
    to prevent repeated failed requests.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_time: int = 60,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time

        self.failure_count = 0
        self.state = "CLOSED"
        self.opened_at = None

    
    def can_execute(self) -> bool:
        """
        Decide whether a request is currently allowed
        to call the external dependency.
        """
        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":
            current_time = time.time()

            if current_time - self.opened_at >= self.recovery_time:
                self.state = "HALF_OPEN"
                return True

            return False

        if self.state == "HALF_OPEN":
            return True

        return False

    def record_failure(self):
        """
        Record a dependency failure.
        """

        if self.state == "CLOSED":
            self.failure_count += 1

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.opened_at = time.time()

        elif self.state == "HALF_OPEN":
            self.state = "OPEN"
            self.opened_at = time.time()
            self.failure_count = self.failure_threshold

    def record_success(self):
        """
        Record a successful dependency call.
        """

        self.state = "CLOSED"
        self.failure_count = 0
        self.opened_at = None


# Test the CircuitBreaker class

# if __name__ == "__main__":
#     breaker = CircuitBreaker(
#         failure_threshold=3,
#         recovery_time=2,
#     )

#     print("Initial:", breaker.state)

#     # Failure 1
#     breaker.record_failure()
#     print("Failure 1:", breaker.state, breaker.failure_count)

#     # Failure 2
#     breaker.record_failure()
#     print("Failure 2:", breaker.state, breaker.failure_count)

#     # Failure 3 → should OPEN
#     breaker.record_failure()
#     print("Failure 3:", breaker.state, breaker.failure_count)

#     # Should block request
#     print("Can execute:", breaker.can_execute())

#     # Wait for recovery period
#     time.sleep(2)

#     # Should move OPEN → HALF_OPEN
#     print("Can execute after recovery:", breaker.can_execute())
#     print("State:", breaker.state)

#     # Simulate successful Supabase probe
#     breaker.record_success()

#     print("After success:", breaker.state, breaker.failure_count)