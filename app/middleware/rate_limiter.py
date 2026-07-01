import os
from fastapi import Request
from fastapi.responses import JSONResponse
import os

from app.core.redis_client import redis_client


class RateLimiterMiddleware:

    def __init__(
        self,
        app
    ):
        self.app = app

    async def __call__(
        self,
        scope,
        receive,
        send
    ):

        if scope["type"] != "http":
            await self.app(
                scope,
                receive,
                send
            )
            return

        # Skip rate limiter during tests
        testing = (
            os.getenv(
                "TESTING",
                "False"
            ) == "True"
        )

        if testing:
            await self.app(
                scope,
                receive,
                send
            )
            return

        request = Request(
            scope,
            receive
        )

        client_ip = (
            request.client.host
        )

        key = (
            f"rate_limit:{client_ip}"
        )

        current_count = (
            redis_client.get(key)
        )

        print("CLIENT IP:", client_ip)
        print("KEY:", key)
        print("CURRENT COUNT:", current_count)

        if current_count:

            current_count = int(
                current_count
            )

            if current_count >= 5:

                response = JSONResponse(
                    status_code=429,
                    content={
                        "detail":
                        "Rate limit exceeded"
                    }
                )

                await response(
                    scope,
                    receive,
                    send
                )

                return

            redis_client.incr(key)

        else:

            redis_client.set(
                key,
                1,
                ex=60
            )

        await self.app(
            scope,
            receive,
            send
        )