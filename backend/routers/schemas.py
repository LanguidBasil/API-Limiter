from pydantic import BaseModel, HttpUrl, IPvAnyAddress, validator
from .dependencies import validate_method


class Bucket_Body(BaseModel):
    url: HttpUrl
    method: str
    ip_address: IPvAnyAddress

    @validator("method")
    def v_method(cls, v: str) -> str:
        return validate_method(v)
