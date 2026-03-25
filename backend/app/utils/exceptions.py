from __future__ import annotations


class AppError(Exception):
    status_code = 400
    detail = "Application error."

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(detail or self.detail)
        self.detail = detail or self.detail


class UnauthorizedError(AppError):
    status_code = 401
    detail = "Unauthorized."


class ForbiddenError(AppError):
    status_code = 403
    detail = "Forbidden."


class NotFoundError(AppError):
    status_code = 404
    detail = "Resource not found."


class ConflictError(AppError):
    status_code = 409
    detail = "Conflict."


class BadRequestError(AppError):
    status_code = 400
    detail = "Bad request."
