
import asyncio
import time
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Async Rate Limiter using a Token Bucket algorithm/Time Window for RPM and RPS.
    Ensures that we do not exceed:
    - max_calls_per_minute (RPM)
    - max_calls_per_second (RPS) - optional
    """

    def __init__(self, rpm: int, rps: float = 0):
        """
        Args:
            rpm: Requests per minute allowed.
            rps: Requests per second allowed (optional). If 0, RPS is not enforced.
        """
        self.rpm = rpm
        self.rps = rps
        
        # RPM Tracking
        self.rpm_period = 60.0  # 1 minute
        self.rpm_tokens = rpm
        self.rpm_updated_at = time.monotonic()
        self.rpm_lock = asyncio.Lock()

        # RPS Tracking
        self.last_request_time = 0.0
        self.rps_interval = 1.0 / rps if rps > 0 else 0
        self.rps_lock = asyncio.Lock()

    async def acquire(self):
        """
        Acquire a slot to make an API call. Waits if limits are reached.
        """
        # 1. Check RPS (Spacing)
        if self.rps > 0:
            async with self.rps_lock:
                now = time.monotonic()
                elapsed = now - self.last_request_time
                wait_time = self.rps_interval - elapsed
                
                if wait_time > 0:
                    logger.debug(f"RateLimiter: Enforcing RPS, waiting {wait_time:.2f}s")
                    await asyncio.sleep(wait_time)
                
                self.last_request_time = time.monotonic()

        # 2. Check RPM (Token Bucket)
        async with self.rpm_lock:
            while True:
                now = time.monotonic()
                time_passed = now - self.rpm_updated_at
                
                # Refill tokens roughly based on time passed
                # Actually, for strict RPM, we might want a sliding window or simpler reset.
                # A simple strict implementation:
                # If we have tokens, take one. If not, wait until we can refill.
                # Let's use a standard token bucket refill.
                
                refill_amount = (time_passed / self.rpm_period) * self.rpm
                if refill_amount > 0:
                    self.rpm_tokens = min(self.rpm, self.rpm_tokens + refill_amount)
                    self.rpm_updated_at = now
                
                if self.rpm_tokens >= 1:
                    self.rpm_tokens -= 1
                    break
                else:
                    # Wait for enough time to get at least 1 token
                    # required_refill = 1 - self.rpm_tokens
                    # time_to_wait = (required_refill / self.rpm) * self.rpm_period
                    # Simplified: wait 1 second and check again to be safe and avoid tight loops
                    wait_time = 60.0 / self.rpm # Wait time for 1 token generated
                    
                    logger.warning(f"RateLimiter: RPM limit reached ({self.rpm} rpm). Waiting {wait_time:.2f}s.")
                    await asyncio.sleep(wait_time)

    async def try_acquire(self) -> bool:
        """
        Try to acquire a token immediately. Returns True if successful, False if rate limited.
        Does NOT wait.
        """
        # 1. Check RPS (Spacing)
        if self.rps > 0:
            async with self.rps_lock:
                now = time.monotonic()
                elapsed = now - self.last_request_time
                wait_time = self.rps_interval - elapsed
                
                if wait_time > 0:
                    return False
                
        # 2. Check RPM (Token Bucket)
        async with self.rpm_lock:
            now = time.monotonic()
            time_passed = now - self.rpm_updated_at
            
            refill_amount = (time_passed / self.rpm_period) * self.rpm
            if refill_amount > 0:
                self.rpm_tokens = min(self.rpm, self.rpm_tokens + refill_amount)
                self.rpm_updated_at = now
            
            if self.rpm_tokens >= 1:
                self.rpm_tokens -= 1
                # Only update last_request_time if we successfully acquired logic token and passed RPS check
                if self.rps > 0:
                     self.last_request_time = time.monotonic()
                return True
            else:
                return False

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        pass
