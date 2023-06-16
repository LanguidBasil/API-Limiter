from pydantic import BaseModel, validator, HttpUrl


class CreateRules_Body(BaseModel):
    urls: list[HttpUrl]
    methods: list[str]
    requests: int
    refresh_rate: int
    
    @validator("urls", "methods")
    def lists_cannot_be_empty(cls, v: list[str]):
        if len(v) < 1:
            raise ValueError("cannot be empty")
        for value in v:
            if not value:
                raise ValueError("value is empty")        
        return v
    
    @validator("urls", "methods")
    def lists_should_be_unique(cls, v: list[str]):        
        if len(set(v)) != len(v):
            raise ValueError("all values should be unique")
        return v
    
    @validator("methods")
    def methods_should_be_case_insensitive(cls, v: list[str]):
        return [s.upper() for s in v]
    
    @validator("requests", "refresh_rate")
    def integers_should_be_more_than_zero(cls, v: int):
        if v < 1:
            raise ValueError("should be more than 0")
        return v
