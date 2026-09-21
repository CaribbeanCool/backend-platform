import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.logging_context import request_id_context


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID")

        if not request_id:
            request_id = str(uuid.uuid4())

        token = request_id_context.set(request_id)

        try:
            request.state.request_id = request_id

            response = await call_next(request)

            response.headers["X-Request-ID"] = request_id

            return response

        finally:
            request_id_context.reset(token)
