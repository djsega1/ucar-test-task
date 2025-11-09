from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    detail: str | None = None
    code: str | None = None
