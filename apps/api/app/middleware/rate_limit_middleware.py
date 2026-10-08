import time

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: int = 10, time_window: int = 60):  
        self.rate_limit = rate_limit  # Set your desired rate limit here
        self.time_window = time_window  # Set your desired time window in seconds here
        self.request_history = {}
        super().__init__(app)


    async def dispatch(self, request, call_next):
        # Get the client IP address
        client_ip = request.client.host

        # Get the current timestamp
        current_time = time.time()


        # Initialize the rate limit data for the client IP if it doesn't exist

        if client_ip not in self.request_history:
            self.request_history[client_ip] = []
        

        # Filter out requests that are outside the time window
        filter_requests = [
                timestamp for timestamp in self.request_history[client_ip] if current_time - timestamp < self.time_window
            ]

        self.request_history[client_ip] = filter_requests

        # Check if the number of requests exceeds the rate limit
        if len(filter_requests) >= self.rate_limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please try again later."},
            )

        self.request_history[client_ip].append(current_time)     

        return await call_next(request)