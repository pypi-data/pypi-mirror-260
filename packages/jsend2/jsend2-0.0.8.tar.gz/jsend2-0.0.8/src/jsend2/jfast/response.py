import json
from typing import TypeVar, Generic, List, Any, Optional
from uuid import UUID
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import JSONResponse

Model = TypeVar("Model", bound=BaseModel)


def get_default_status() -> str:
    return "success"


class JsendBase:
    status: Optional[str] = None
    data: Optional[Any] = None

    # Error
    code: Optional[int] = None
    message: Optional[str] = None

    #  Pagination
    total: Optional[int] = None
    count: Optional[int] = None
    offset: Optional[int] = None


class JsendResponse(JsendBase, BaseModel):
    pass


class BaseGenericResponse(GenericModel, JsendBase):
    status: str = Field(default_factory=get_default_status)
    message: Any | None


class BaseGenericResponse(GenericModel, JsendBase):
    status: str = Field(default_factory=get_default_status)
    message: Any | None
    status_code: Optional[int] = None  # Add status_code attribute


class GenericSingleResponse(BaseGenericResponse, Generic[Model]):
    data: Model


class GenericMultipleResponse(BaseGenericResponse, Generic[Model]):
    data: List[Model]


class ResponseMultiple(GenericMultipleResponse, GenericModel, Generic[Model]):
    pass


class Response(GenericSingleResponse, GenericModel, Generic[Model]):
    pass


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def render_jsend(data: dict, status_code: int = status.HTTP_200_OK, **kwargs):
    custom_encoder = kwargs.get("encoder")
    encoder = UUIDEncoder
    if custom_encoder:
        encoder = custom_encoder
    jsend_data = JsendResponse(data=data).__dict__
    content = json.loads(json.dumps(jsend_data, cls=encoder))
    return JSONResponse(content=content, status_code=status_code)

# class GenericErrorResponse(BaseGenericResponse, Generic[Model]):
#     data: Any
# class ErrorResponse(GenericErrorResponse, GenericModel, Generic[Model]):
#     pass
