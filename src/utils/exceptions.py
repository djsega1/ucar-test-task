from starlette import status

from src.schemas.exceptions import ErrorResponse


class BaseAPIException(Exception):
    message: str
    status_code: int
    detail: str | None
    error_code: str | None

    def __init__(
        self,
        detail: str | None = None,
    ) -> None:
        self.detail = detail
        super().__init__(self.message)

    def to_response(self) -> ErrorResponse:
        return ErrorResponse(
            message=self.message,
            detail=self.detail,
            code=self.error_code,
        )


class NotFoundException(BaseAPIException):
    message = 'Resource not found'
    status_code = status.HTTP_404_NOT_FOUND
    code = 'NOT_FOUND'


class ValidationException(BaseAPIException):
    message = 'Validation error'
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    code = 'UNPROCESSABLE_CONTENT'
