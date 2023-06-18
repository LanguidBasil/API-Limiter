from pydantic import BaseModel, validator, HttpUrl

from ...utils import HTTPMethod


class GetRules_Body(BaseModel):
    url: HttpUrl | None
    method: HTTPMethod | None

class CreateRules_Body(BaseModel):
    urls: list[HttpUrl]
    methods: list[HTTPMethod]
    requests: int
    refresh_rate: int
    
    @validator("urls", "methods")
    def v_lists_cannot_be_empty(cls, v: list[str]) -> list[str]:
        if len(v) < 1:
            raise ValueError("cannot be empty")
        return v
    
    @validator("urls", "methods")
    def v_lists_should_be_unique(cls, v: list[str]) -> list[str]:
        if len(set(v)) != len(v):
            raise ValueError("all values should be unique")
        return v
    
    @validator("requests", "refresh_rate")
    def v_integers_should_be_more_than_zero(cls, v: int) -> int:
        if v < 1:
            raise ValueError("should be more than 0")
        return v

class DeleteRules_Body(BaseModel):
    url: HttpUrl
    method: HTTPMethod
