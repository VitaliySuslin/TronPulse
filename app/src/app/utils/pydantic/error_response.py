from typing import Optional, Any

from pydantic import BaseModel, Field


class DetailDefaultErrorResponseSchema(BaseModel):
    description: Optional[str] = Field(description="A clear explanation for everyone.")
    obj: Optional[str] = Field(default=None)
    context: Optional[Any] = Field(description="Additional information", default=None)


class DefaultErrorResponseSchema(BaseModel):
    code: Optional[int] = Field(description="Internal error code")
    message: Optional[str] = Field(description="Description")
    detail: Optional[DetailDefaultErrorResponseSchema] = Field(description="Error details")