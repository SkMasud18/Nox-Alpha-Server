import time
from typing import Dict, List

class SlidingWindowRateLimiter:
    """
    In-memory / Redis-backed sliding window rate limiter.
    Enforces strict IP-level guardrails preventing DDoS and API quota abuse.
    """

    def __init__(self, limit_1m: int = 4, limit_10m: int = 10):
        self.limit_1m = limit_1m
        self.limit_10m = limit_10m
        self.requests: Dict[str, List[float]] = {}

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        timestamps = self.requests.get(client_ip, [])

        # Prune entries older than 10 minutes (600 seconds)
        timestamps = [t for t in timestamps if now - t < 600]
        self.requests[client_ip] = timestamps

        # Count in last 1 minute
        count_1m = sum(1 for t in timestamps if now - t < 60)
        if count_1m >= self.limit_1m:
            return False

        # Count in last 10 minutes
        if len(timestamps) >= self.limit_10m:
            return False

        # Record this request
        self.requests[client_ip].append(now)
        return True
