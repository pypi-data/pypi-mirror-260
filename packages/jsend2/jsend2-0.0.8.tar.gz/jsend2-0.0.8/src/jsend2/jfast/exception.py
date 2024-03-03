import os

from fastapi import HTTPException
from starlette.responses import JSONResponse

from .response import JsendResponse


class ExceptionMiddleware:
    def __init__(self, app) -> None:
        self.app = app
        self.app.add_exception_handler(HTTPException, self.http_exception_handler)
        self.app.add_exception_handler(Exception, self.exception_handler)

    def http_exception_handler(self, request, exc):
        payload = JsendResponse(
            status="error",
            message=exc.detail,
        )
        response = JSONResponse(
            payload.model_dump(exclude_none=True), status_code=exc.status_code
        )
        return response

    def exception_handler(self, request, exc):
        payload = JsendResponse(
            status="error",
            message=str(exc),
        )
        if os.environ.get("DEBUG") == "1":
            payload.message = str(exc)
        else:
            payload.message = "InternalError"

        response = JSONResponse(payload.model_dump(exclude_none=True), status_code=500)
        return response
