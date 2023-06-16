from pydantic import BaseModel, HttpUrl, IPvAnyAddress, validator

from ..dependencies import validate_method


class Validate_Body(BaseModel):
    url: HttpUrl
    method: str
    ip_address: IPvAnyAddress
    
    # TODO: for some reason on ValueError it does not create beautiful 422 message
    @validator("method")
    def v_method(cls, v: str) -> str:
        return validate_method(v)

class Validate_Response(BaseModel):
    is_allowed: bool
    requests_left: int | None
    seconds_to_next_refresh: float | None

